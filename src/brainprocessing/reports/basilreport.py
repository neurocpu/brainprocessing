import dominate
from dominate.tags import *
import datetime
import nibabel
import os
from nilearn import plotting


def create_document(title, stylesheet=None, script=None):
    doc = dominate.document(title = title)
    if stylesheet is not None:
        with doc.head:
            link(rel='stylesheet',href=stylesheet)
    if script is not None:
        with doc.head:
            script(type='text/javascript',src=script)
    with doc:
        with div(id='header'):
            h1(title)
            p('Report generated on {}'.format(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%dT%H:%M:%S.%f')) )
    return doc

def create_section(doc, divid, divclass, captiontext):
    with doc:
        if divclass is None:
            d = div(id=divid)
        else:
            d = div(id=divid, cls=divclass)
        with d:
            h2(captiontext)
    return doc

def add_image(doc, divid, divclass, captiontext, image):
    with doc:
        if divclass is None:
            d = div(id=divid)
        else:
            d = div(id=divid, cls=divclass)
        with d:
            h3(captiontext)
            img(src=image)
    return doc

def writeContourImageSequence(contour_img_filename, png_file, levellist=[0.5],colors=['r','g','b','y','m','c']):
    contour_img = nibabel.load(contour_img_filename)
    if len(contour_img.header.get_data_shape()) > 3:
        contour_list = nibabel.funcs.four_to_three(contour_img)
        contour_bg_img = contour_list[0]

        mycanvas=plotting.plot_anat(contour_bg_img)

        colorcount=0
        colorsize=len(colors)
        for contour_img in contour_list[1:]:
            colornum=colorcount%colorsize
            mycanvas.add_contours(contour_img,levels=levellist,colors=colors[colornum])
            colorcount=colorcount+1
            
        mycanvas.savefig(png_file)

def writeContourImage(bg_img_filename, contour_img_filename, png_file, levellist=[0.5],colors='r'):
    bg_img = nibabel.load(bg_img_filename)
    if len(bg_img.header.get_data_shape()) > 3:
        bg_list = nibabel.funcs.four_to_three(bg_img)
        bg_img = bg_list[0]

    contour_img = nibabel.load(contour_img_filename)
    if len(contour_img.header.get_data_shape()) > 3:
        contour_list = nibabel.funcs.four_to_three(contour_img)
        contour_img = contour_list[0]

    mycanvas=plotting.plot_anat(bg_img)
    mycanvas.add_contours(contour_img,levels=levellist,colors=colors)
    mycanvas.savefig(png_file)

def createMotionSection(doc,datadir,titles,imagedir):

    if not os.path.exists(imagedir):
        os.makedirs(imagedir)
        
    asldatapre=os.path.join(datadir,'asldata_orig.nii.gz')
    image1=os.path.join(imagedir,'asldatapre.png')
    asldatapost=os.path.join(datadir,'asldata.nii.gz')
    image2=os.path.join(imagedir,'asldatapost.png')

    writeContourImageSequence(asldatapre,image1, levellist=[10,20,50,100])
    writeContourImageSequence(asldatapost,image2, levellist=[10,20,50,100])

    doc = add_image(doc, titles[0], None, 'pre motion corr', image1)

    doc = add_image(doc, titles[1], None, 'post motion corr', image2)


    return doc

def createStructRegSection(doc,datadir,titles,imagedir):

    if not os.path.exists(imagedir):
        os.makedirs(imagedir)

    struct=os.path.join(datadir,'struc.nii.gz')
    struct_bet_mask=os.path.join(datadir,'struc_bet_mask.nii.gz')
    image1=os.path.join(imagedir,'bet2struct.png')
    calib=os.path.join(datadir,'calib_struc.nii.gz')
    image2=os.path.join(imagedir,'calib2struct.png')
    asl=os.path.join(datadir,'asl2struct.nii.gz')
    image3=os.path.join(imagedir,'asl2struct.png')

    writeContourImage(struct,struct_bet_mask,image1)
    writeContourImage(calib,struct_bet_mask,image2)
    writeContourImage(asl,struct_bet_mask,image3)

    doc = add_image(doc, titles[0], None, 'registration of bet to struct', image1)

    doc = add_image(doc, titles[1], None, 'registration of calib to struct', image2)

    doc = add_image(doc, titles[2], None, 'registration of asl to struct', image3)

    return doc


def createProcReport(stylesheet, imagedir, datadir, title):
    """
    Main Function reate the

    """
    doc = create_document(title, stylesheet)
    with doc:
        with div(id='links').add(ul()):
            h2('Contents')
            li(a('Structural Registration',href='#structuralreg'))
            nested=ul()
            with nested:
                for i in ['bet2struct', 'calib2struct','asl2struct']:
                    li(a(i.title(), href='#%s' % i))
            li(a('Motion QC',href='#motionqc'))
            nested=ul()
            with nested:
                for i in [ 'asldata_pre', 'asldata_post']:
                    li(a(i.title(), href='#%s' % i))

    doc += hr()
    doc = create_section(doc, 'structuralreg', None, 'Structural Registration')
    doc += hr()
    doc = createStructRegSection(doc, datadir, ['bet2struct','calib2struct', 'asl2struct'],imagedir)
    doc += hr()
    doc = create_section(doc, 'motionqc', None, 'Motion QC')
    doc += hr()
    doc = createMotionSection(doc, datadir, [ 'asldata_pre', 'asldata_post'],imagedir)


    return doc


if __name__ == '__main__':
    """
    usage: basilreport.py [stylefile] [imagedir] [filedir] [outputfile]
    python basilreport.py ./example/style.css ./example/images ./example/data ./example/final.html

    """
    import sys
    from standalone_html import make_html_images_inline 
    stylefile=os.path.abspath(sys.argv[1])
    #stylefile='./example/style.css'
    imagedir=os.path.abspath(sys.argv[2])
    #imagedir='./example/images'
    filedir=os.path.abspath(sys.argv[3])
    #filedir = './example/data'
    outputfile=os.path.abspath(sys.argv[4])
    doc = createProcReport(stylefile, imagedir, filedir, 'Basil Report')
    final_report_html = outputfile
    final_report_inline_html = outputfile.split(".")[0] + "_inline.html"
    with open(final_report_html, 'w') as file:
        file.write(doc.render())
    make_html_images_inline(final_report_html, final_report_inline_html)




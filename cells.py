from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import time
import os
import os.path

def main():
    search_fiji.fiji_path = 'ffiji-win64\Fiji.app\ImageJ-win64.exe'
    image.image_filename = ''
    data.data_filename = ''
    classifier.classifier_filename = ''
    fenetre = Tk()
    fenetre.title('Cells')
    fenetre.iconbitmap(r'files/icon.ico')
    fenetre.resizable(width=False, height=False)

    fenetre.minsize(800, 500)

    main.button1=Button(fenetre, text="Charger l'Image", command=image)
    main.button1.pack()
    main.button1.place(x = 0, y = 0)
    main.button2=Button(fenetre, text="Charger les données", command=data)
    main.button2.pack()
    main.button2.config(state=DISABLED)
    main.button2.place(x = 100, y = 0)
    main.button3=Button(fenetre, text="Charger le Classifier", command=classifier)
    main.button3.pack()
    main.button3.config(state=DISABLED)
    main.button3.place(x = 223, y = 0)
    main.button4=Button(fenetre, text="Run", command=run)
    main.button4.pack()
    main.button4.config(state=DISABLED)
    main.button4.place(x = 765, y = 0)



    menubar = Menu(fenetre)

    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label="Run", command=run)
    menu1.add_separator()
    menu1.add_command(label="Quitter", command=fenetre.quit)
    menubar.add_cascade(label="Fichier", menu=menu1)

    fenetre.config(menu=menubar)


    fenetre.mainloop()


def classifier():
    classifier.classifier_filename = askopenfilename(title="Ouvrir le Classifier", filetypes=[('Fichier MODEL', '.model'), ('tous les fichiers', '.*')])
    if classifier.classifier_filename == '':
    	showerror('Cells', "Vous n'avez pas séléctionné de fichier")
    else:
    	showinfo('Cells', "Le Classifier a été ajouté avec succès!")
    	main.button4.config(state=NORMAL)


def data():
    data.data_filename = askopenfilename(title="Ouvrir la Data", filetypes=[('Fichier ARFF', '.arff'), ('tous les fichiers', '.*')])
    if data.data_filename == '':
    	showerror('Cells', "Vous n'avez pas séléctionné de données")
    else:
    	showinfo('Cells', "Les données ont été ajoutées avec succès!")
    	main.button3.config(state=NORMAL)

def image():
    image.image_filename = askopenfilename(title="Ouvrir l'Image", filetypes=[('Fichier TIFF', '.tif'), ('tous les fichiers', '.*')])
    if image.image_filename == '':
    	showerror('Cells', "Vous n'avez pas séléctionné d'Image")
    else:
        showinfo('Cells', "L'Imge a été ajoutée avec succès!")
        main.button2.config(state=NORMAL)
        os.startfile(image.image_filename)

def launch_fiji():
    os.system(search_fiji.fiji_path + ' -macro files\cells_macro.ijm')
def search_fiji():
    if os.path.isfile(search_fiji.fiji_path):
    	launch_fiji()
    else:
    	showerror('Cells', "Fiji n'a pas été trouvé, veuillez indiquer son chemin")
    	search_fiji.fiji_path = askopenfilename(title="Fiji", filetypes=[('Fichier EXE', '.exe'), ('tous les fichiers', '.*')])
    	launch_fiji()


def run():

    image_name_list = image.image_filename.split('/')
    image_name = image_name_list[-1]

    macro = "open('" + image.image_filename + "');run('Duplicate...', ' ');selectWindow('" + image_name + "');run('Trainable Weka Segmentation');selectWindow('Trainable Weka Segmentation v3.2.23');call('trainableSegmentation.Weka_Segmentation.loadClassifier', '" + classifier.classifier_filename + "');wait(1000);call('trainableSegmentation.Weka_Segmentation.loadData', '" + data.data_filename + "');wait(1000);call('trainableSegmentation.Weka_Segmentation.getProbability');wait(1000);selectWindow('Probability maps');setThreshold(0.99, 1.0000);setOption('BlackBackground', true);run('Convert to Mask', 'method=Default background=Dark calculate black');run('Watershed', 'slice');run('Set Measurements...', 'area perimeter bounding shape redirect=None decimal=3');run('Analyze Particles...', 'size=5-Infinity show=Outlines display exclude clear add in_situ slice');selectWindow('image-1.tif');roiManager('Show All');run('Flatten');run('Save', 'save=[" + image.image_filename + "_ROI.tif]');"

    if classifier.classifier_filename == '' or image.image_filename == '' or data.data_filename == '':
        showerror('Cells', "Vous avez oublié de sélécionner une data ou un classifier ou une image")
    else:
        f = open('files/cells_macro.ijm', 'w')
        f.write(macro)
        f.close()
        search_fiji()


if __name__ == '__main__':
    main()

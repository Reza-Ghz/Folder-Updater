#!/usr/bin/python3.5
import shutil, os
import platform
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import threading
from multiprocessing import Process, Manager, Queue
import time
#from threading import _thread



global version
version=1.0

global x, y,progress,value,restart  # global variables for count files and folders

progress,value,restart=0,0,True

global source_dir_path,destination_dir_path

source_dir_path=''
destination_dir_path=''
class folder_updater:

    def __init__(self,master):
        global source_dir_path,destination_dir_path

        #window configuration
        self.master=master
        master.title('Folder Updater')
        #master.iconbitmap(default='logo.ico')   #icon(Doesn't work on Linux)
        master.resizable(False,False)
        master.configure(background='#8cc3e7')
        master.geometry('685x420+500+200')
        master.option_add('*tearOff',False)


        #creat menu bars
        self.menu_bar=Menu(master)
        self.file=Menu(self.menu_bar)
        self.help=Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu = self.file ,label='File')
        self.menu_bar.add_cascade(menu = self.help,label='Help')
        self.file.add_command(label='Exit',command=lambda: self.exit_bottun_command(1))
        self.help.add_command(label='About', command=lambda: self.help_button_command())
        master.config(menu=self.menu_bar)  # display menu bar

        #creat styles
        self.style=ttk.Style()
        self.style.configure('TFrame',background='#8cc3e7')
        self.style.configure('TButton', background='#8cc3e7')
        self.style.configure('TLabel', background='#8cc3e7',foreground='black',font=('Arial',11))
        self.style.configure('header.TLabel',font=('courier', 38,'bold'))
        self.style.configure('other.TLabel', font=('Arial', 12,'bold'))
        self.style.configure('other.TButton', font=('arial', 13))
        self.style.configure('all_right.TLabel', font=('arial', 9))



        #creat frame 
        self.frame_header=ttk.Frame(master)
        self.frame_header.pack()

        #self.logo=PhotoImage(file='logo.png')
        #ttk.Label(self.frame_header,image=self.logo).grid(row=0,column=1,rowspan=2,padx=10)
        ttk.Label(self.frame_header,text='FOLDER UPDATER',style='header.TLabel').grid(row=0,column=0,sticky='s',padx=5)
        ttk.Label(self.frame_header,text='A cross-platform folder sync tool',wraplength=300,font=(15),style='header.TLabel').grid(row=1,column=0,sticky='n')

        self.frame_input=ttk.Frame(master)
        self.frame_input.pack()

        #add labels
        ttk.Label(self.frame_input, text='Please select your source and '
                                         'destination folder and '
                                         'press "start" button:'
                  ,font=('Arial',13),wraplength=600).grid(row=0,column=0,columnspan=5,padx=5,pady=20)


        ttk.Label(self.frame_input,text='Source Directory:',style='other.TLabel').grid(row=2,column=0,padx=5,pady=1,sticky='e')
        ttk.Label(self.frame_input, text='Destination Directory:',style='other.TLabel').grid(row=3,column=0,padx=5,pady=1,sticky='e')
        ttk.Label(self.frame_input, text='@All right reserved to Alireza.Gh 2017',style='all_right.TLabel').grid(row=7, column=0, padx=0,pady=0, sticky='w')

        self.source_entry=ttk.Entry(self.frame_input,width=45,font=('Arial',10))
        try:
            self.source_entry.config(state='enabled')
            self.source_entry.insert(0, source_dir_path)
            self.source_entry.config(state='disabled')
        except:
            pass

        self.destination_entry= ttk.Entry(self.frame_input, width=45,font=('Arial',10))
        try:
            self.destination_entry.config(state='enabled')
            self.destination_entry.insert(0, destination_dir_path)
            self.destination_entry.config(state='disabled')
        except:
            pass

        #default configuration for entries and buttons
        self.source_entry.grid(row=2,column=1,columnspan=2,padx=5,sticky='w')
        self.destination_entry.grid(row=3,column=1,columnspan=2,padx=5,sticky='w')
        self.source_entry.config(state='disabled')
        self.destination_entry.config(state='disabled')




        self.source_browse_button=ttk.Button(self.frame_input,text='Browse',command=lambda: self.browse_button_command('source')).grid(row=2,column=3,padx=5)
        self.destination_browse_button = ttk.Button(self.frame_input, text='Browse',command=lambda: self.browse_button_command('dest')).grid(row=3,column=3,padx=5)


        self.start_button = ttk.Button(self.frame_input, text='Start',command=lambda: self.start_button_command(),style='other.TButton').grid(row=6, column=1,padx=10,pady=40,sticky='e')
        self.exit_button = ttk.Button(self.frame_input, text='Exit',command=lambda: self.exit_bottun_command(1),style='other.TButton').grid(row=6, column=2,padx=10,pady=40,sticky='w')



        self.cansel_flag=False
        self.result='W8'
        self.source_dir_path=source_dir_path
        self.destination_dir_path=destination_dir_path

    #soruce and dest directory
    def browse_button_command(self,which_calling):
        global  source_dir_path,destination_dir_path

        if which_calling=='source':
            self.source_dir_path_newer= filedialog.askdirectory()

            if not self.source_dir_path_newer=='':
                self.source_dir_path=self.source_dir_path_newer
                source_dir_path=self.source_dir_path
            if not self.source_dir_path=='':
                self.source_entry.config(state='enabled')
                self.source_entry.delete(0, END)
            self.source_entry.config(state='enabled')
            self.source_entry.insert(0,self.source_dir_path)
            self.source_entry.config(state='disabled')

        elif which_calling=='dest':
            self.destination_dir_path_newer= filedialog.askdirectory()
            if not self.destination_dir_path_newer=='':
                self.destination_dir_path=self.destination_dir_path_newer
                destination_dir_path=self.destination_dir_path
            if not self.destination_dir_path == '':
                self.destination_entry.config(state='enabled')
                self.destination_entry.delete(0, END)
            self.destination_entry.config(state='enabled')
            self.destination_entry.insert(0, self.destination_dir_path)
            self.destination_entry.config(state='disabled')


    #start the updating
    def start_button_command(self):
        global progress,value
        self.cansel_flag = False
        progress = 0
        value=0

        global x,y
        x = 0
        y = 0


        #check the source and dest 
        if self.source_dir_path=='' or self.destination_dir_path=='':
            messagebox.showwarning(title='Folder Updater', message='Please enter your "Source directory" and "Destination directory" before start.')
            return
        elif self.source_dir_path==self.destination_dir_path:
            messagebox.showwarning(title='Folder Updater', message='"Source directory" and "Destination directory" are the same,change your source or destination directory.')
            return

        #creates new window
        self.frame_header.pack_forget()
        self.frame_input.pack_forget()

        self.master.geometry('620x483+500+200')

        self.frame_progress=ttk.Frame(self.master)
        self.frame_progress.pack()


        ttk.Label(self.frame_progress, text='Folders are updating it might takes several minutes...'
                    ,font=('Arial',18),wraplength=600).grid(row=0, column=0,padx=5,columnspan=2)

        ttk.Label(self.frame_progress, text='(If you press cancel,progress will save)'
                  , font=('Arial', 15), wraplength=600).grid(row=1, column=0, padx=5,sticky='w')
        ttk.Label(self.frame_progress, text='@All right reserved to Alireza.Gh 2017',style='all_right.TLabel').grid(row=4, column=0, padx=0, pady=0,
                                                                                       sticky='ws')

        #adding progress bar
        self.progress_bar=ttk.Progressbar(self.frame_progress,orient=HORIZONTAL,length=563.8)
        self.progress_bar.grid(row=2,column=0,columnspan=2,pady=20)
        self.progress_bar.config(mode='determinate')#maximum value should give value



        self.progress_text=Text(self.frame_progress,width=70,height=18)
        self.progress_text.grid(row=3,column=0,columnspan=2,padx=5)
        self.progress_text.config(background='black',foreground='white')
        self.progress_text.config(wrap='none')
        #self.progress_text.insert('end','asdadsadasdadsadasdsada\nadasdadadadab') #should give the string

        #self.progress_text.config(state='disabled')# should enable before inset

        self.scroll_bary = ttk.Scrollbar(self.frame_progress, orient=VERTICAL, command=self.progress_text.yview)
        self.scroll_barx = ttk.Scrollbar(self.frame_progress, orient=HORIZONTAL, command=self.progress_text.xview)
        self.scroll_bary.grid(row=3, column=1, sticky='ens')
        self.scroll_barx.grid(row=4, column=0, columnspan=2, sticky='ewn', padx=10)
        self.progress_text.configure(yscrollcommand=self.scroll_bary.set)
        self.progress_text.configure(xscrollcommand=self.scroll_barx.set)


        self.finish_button=ttk.Button(self.frame_progress,text='Cancel',command=lambda: self.cancel_button_command(0),style='other.TButton')
        self.finish_button.grid(row=4,column=1,pady=20)




        #creates new threat but still have problem in loop to rendering the windows
        messagebox.showwarning(title='Folder Updater',message='For big files app will freez until file copy complete,so its working correctly dont worry.')
        self.the_thread=threading.Thread(target=self.start_updating(),args=())
        self.the_thread.start()
        self.the_thread._stop()
        #self.master.after(0,self.start_updating)
        #thread.start_new_thread(self.start_updating(),())


        


        self.progress_text.config(state='disabled')
        self.finish_button.config(text='Finish')#change name of cancel buton
        #messagebox.showinfo(title='Folder Updater',message='Update Finished!')
        #messagebox.showwarning(title='Folder Updater',message="acces denied!")

    def start_updating(self):

        global x,y

        self.log_result = self.log_creater()
        if not self.log_result == 0:
            self.result = self.heart(self.source_dir_path, self.destination_dir_path, self.log, self.os_name)
            if self.result == 0:
                print("=================================================================\n")
                print('   ERROR:   Something bad happed update didnt finish correctly!\n')
                print("=================================================================\n")
                self.log.write("=================================================================\n")
                self.log.write('   ERROR:   Something bad happed update didnt finish correctly!\n')
                self.log.write("=================================================================\n")
                self.progress_text.insert('end', "=================================================================\n")
                self.progress_text.insert('end', '   ERROR:   Something bad happed update didnt finish correctly!\n')
                self.progress_text.insert('end', "=================================================================\n")
                messagebox.showinfo(title='Folder Updater', message='Update Finished but have some errors check "log file"(FolderUpdaterLOG.txt) in:\n {}'.format(self.destination_dir_path))
                self.log.close()
            elif self.result == 1:

                if x == 0 and y == 0:
                    print("=================================================================\n")
                    print('            Finished: All folders are up to date\n')
                    print("=================================================================\n")
                    self.log.write("=================================================================\n")
                    self.log.write('            Finished: All folders are up to date\n')
                    self.log.write("=================================================================\n")
                    self.progress_text.insert('end',
                                              "=================================================================\n")
                    self.progress_text.insert('end', '            Finished: All folders are up to date\n')
                    self.progress_text.insert('end',
                                              "=================================================================\n")
                    messagebox.showinfo(title='Folder Updater', message='Update Finished!')
                else:
                    print(
                        "===============================================================================================================\n")
                    print(
                        '            Finished: Gz,all folders updated...[{} file(s) coppied and {} folder(s) created\n'.format(
                            x, y))
                    print(
                        "===============================================================================================================\n")
                    self.log.write(
                        "===============================================================================================================\n")
                    self.log.write(
                        '            Finished: Gz,all folders updated...[{} file(s) coppied and {} folder(s) created\n'.format(
                            x, y))
                    self.log.write(
                        "===============================================================================================================\n")
                    self.progress_text.insert('end',
                                              "===============================================================================================================\n")
                    self.progress_text.insert('end',
                                              '            Finished: Gz,all folders updated...[{} file(s) coppied and {} folder(s) created\n'.format(
                                                  x, y))
                    self.progress_text.insert('end',
                                         "===============================================================================================================\n")
                    messagebox.showinfo(title='Folder Updater', message='Update Finished!')
                self.log.close()
                return

    def cancel_button_command(self,permisson):




        if permisson==0 and not self.finish_button['text']=='Finish':
            ask_sure=messagebox.askyesno(title='Folder Updater',message='Are you sure to cansel this procces?')
            if ask_sure == True :
                self.cansel_flag = True
                messagebox.showinfo(title='Folder Updater',message='Progress will cansel as soon as possible,check "log file"(FolderUpdaterLOG.txt) in:\n {}'.format(self.destination_dir_path))
                try:
                    self.the_thread._stop()
                except:
                    pass
                self.exit_bottun_command(0)

                # self.frame_progress.pack_forget()
                # self.frame_header.pack()
                # self.frame_input.pack()
                # self.master.geometry('685x420+500+200')



        if  permisson==1 or self.finish_button['text']=='Finish':
            try:
                self.the_thread._stop()
            except:
                pass
            self.exit_bottun_command(0)
            # self.frame_progress.pack_forget()
            # self.frame_header.pack()
            # self.frame_input.pack()
            # self.master.geometry('685x420+500+200')



        else :
            return


    def help_button_command(self):
        global version

        help_window=Toplevel(self.master)
        help_window.title("About")
        help_window.resizable(False,False)
        help_window.geometry("300x180+650+350")
        help_window.configure(background='#8cc3e7')

        ttk.Frame(help_window).pack()
        ttk.Label(help_window,text='Folder Updater  ver.{}\n\nThis application made by Alireza.Gh \n If you see any bug send it to me in:\n ''siralirezagh@gmail.com\n @seralireza \n'.format(version),style='other.TLabel').pack()
        ttk.Button(help_window,text="Ok",command=lambda :help_window.destroy()).pack()
        #messagebox.showinfo(title='Folder Updater', message='Folder Updater  ver.{}\nThis application made by Alireza.Gh \n\n If you see any bug send it to me in:\n ''siralirezagh@gmail.com\n @seralireza '.format(version))

    def exit_bottun_command(self,who):
        global  restart
        if who==0:
            self.master.destroy()
            return
        # else:
        #     ask_sure = messagebox.askyesno(title='Folder Updater', message='Do you want exit Folder Updater?')
        #
        #     if ask_sure == True:
        self.master.destroy()
        restart=False
            # else:
            #     return


    def refresh(self):
        self.master.update()
        self.master.after(5,self.refresh)

    def log_creater(self):

        self.os_name = platform.system()
        if self.os_name == 'Windows':
            print("You are running program on Windows")
            self.progress_text.insert('end', 'You are running program on Windows\n')
        if self.os_name == 'Linux':
            print("You are running program on Linux")
            self.progress_text.insert('end', 'You are running program on Linux\n')
        if self.os_name == 'Mac':
            print("You are running program on Mac")
            self.progress_text.insert('end', 'You are running program on Mac\n')

        self.check_to_creat_log = True
        try:
            if self.os_name == 'Windows':
                self.log = open(self.destination_dir_path + "\\FolderUpdaterLOG.txt", 'w+')  # creat a log text file
                self.progress_text.insert('end','Log file(FolderUpdaterLOG.txt) created in root of destination folder.\n')
            else:
                self.log = open(self.destination_dir_path + "/FolderUpdaterLOG.txt", 'w+')
        except PermissionError:
            print('Acces denied to creat log file please enter another path or run program as root/admin permisson.\n')
            #self.progress_text.insert('end', 'Acces denied to creat log file please enter another path or run program as root/admin permisson.\n')
            messagebox.showwarning(title='Folder Updater', message="Acces denied to creat log file please enter another path or\n"
                                                                   "run program with ROOT/ADMIN permission")
            self.cancel_button_command(1)
            return 0
        except :
            print('Destionation directory doesnt exits or something else.can not make "LOG" file please check your directories.\n')
            #self.progress_text.insert('end', 'Acces denied to creat log file please enter another path or run program as root/admin permisson.\n')
            messagebox.showwarning(title='Folder Updater', message='Destionation directory doesnt exits or something else.can not make "LOG" file please check your directories.\n')
            self.cancel_button_command(1)
            return 0

    def heart(self,source_dir_path, destionation_dir_path, log, os_name):

        if self.cansel_flag==True:
            return 2
        global x, y,progress,value
        #erorr handling for source dir
        try:
            os.chdir(source_dir_path)
        except FileNotFoundError:
            print("source directory({}) doesnt exist! Please enter the right path...\n".format(source_dir_path))
            log.write("source directory({}) doesnt exist! Please enter the right path...\n".format(source_dir_path))
            messagebox.showwarning(title='Folder Updater',message='source directory({}) doesnt exist! Please enter the right path...'.format(source_dir_path))
            self.progress_text.insert('end',"source directory({}) doesnt exist! Please enter the right path...\n".format(source_dir_path))
            return 0
        except PermissionError:
            print('Acces denied to source directory({}) please enter another path or run program as root/admin permisson\n'.format(source_dir_path))
            log.write('Acces denied to source directory({}) please enter another path or run program as root/admin permisson\n'.format(source_dir_path))
            messagebox.showwarning(title='Folder Updater', message='Acces denied to source directory({}) please enter another path or run program as root/admin permisson!'.format(source_dir_path))
            self.progress_text.insert('end',"source directory({}) doesnt exist! Please enter the right path...\n".format(source_dir_path))
            return 0
        except:
            print('Something wrong ... check your directories and restart the program.')
            log.write('Something wrong ... check your directories and restart the program.')
            messagebox.showwarning(title='Folder Updater', message='Something wrong ... check your directories and restart the program.')
            self.progress_text.insert('end', 'Something wrong ... check your directories and restart the program.')
            return 0
        if self.cansel_flag==True:
            return 2
        self.master.update()
        # saving source list of files and folders in this variable
        source_folders_list = next(os.walk('.'))[1]
        source_folders_list_backup = next(os.walk('.'))[1]
        source_files_list = next(os.walk('.'))[2]

        # Error handling for dest directory
        try:
            os.chdir(destionation_dir_path)
        except FileNotFoundError:
            print("destination directory({}) doesnt exist! Please enter the right path...\n".format(destionation_dir_path))
            log.write("destination directory({}) doesnt exist! Please enter the right path...\n".format(destionation_dir_path))
            #messagebox.showwarning(title='Folder Updater', message='destination directory({}) doesnt exist! Please enter the right path...'.format(destionation_dir_path))
            self.progress_text.insert('end',"destination directory({}) doesnt exist! Please enter the right path...\n".format(destionation_dir_path))
            return 0
        except PermissionError:
            print('Acces denied to destination directory({}) please enter another path or run program as root/admin permisson\n'.format(destionation_dir_path))
            log.write('Acces denied to destination directory({}) please enter another path or run program as root/admin permisson\n'.format(destionation_dir_path))
            #messagebox.showwarning(title='Folder Updater', message='Acces denied to destination directory({}) please enter another path or run program as root/admin permisson'.format(destionation_dir_path))
            self.progress_text.insert('end','Acces denied to destination directory({}) please enter another path or run program as root/admin permisson\n'.format(destionation_dir_path))
            return 0
        except:
            print('Something wrong ... check your directories and restart the program.')
            log.write('Something wrong ... check your directories and restart the program.')
            #messagebox.showwarning(title='Folder Updater', message='Something wrong ... check your directories and restart the program.')
            self.progress_text.insert('end','Something wrong ... check your directories and restart the program.')
            return 0
        self.master.update()

        if self.cansel_flag==True:
            return 2
        # saving destination list of files and folders in this variable
        destination_folders_list = next(os.walk('.'))[1]
        destination_files_list = next(os.walk('.'))[2]

        # finding common files and folders
        common_folders = list(set(source_folders_list).intersection(destination_folders_list))
        common_files = list(set(source_files_list).intersection(destination_files_list))

        # removing common items from source list
        for item in common_folders:
            if self.cansel_flag == True:
                return 2
            source_folders_list.remove(item)
        print('\n\nIN DIRECTORY: >> {}\n'.format(destionation_dir_path))
        log.write('\n\nIN DIRECTORY: >> {}\n'.format(destionation_dir_path))
        self.progress_text.insert('end', '\n\nIN DIRECTORY: >> {}\n'.format(destionation_dir_path))
        self.master.update()
        # creats folders
        for folder in source_folders_list:
            if self.cansel_flag == True:
                return 2
            try:
                try:
                    os.mkdir(folder)
                    y += 1
                    print("DONE:Folder ==| {} |== has bin created.\n".format(folder))
                    log.write("DONE:Folder ==| {} |== has bin created.\n".format(folder))  # writes in log file
                    self.progress_text.insert('end',"DONE:Folder ==| {} |== has bin created.\n".format(folder))

                except PermissionError:
                    print("=============================================================================================\n")
                    print('     SKKIPED:Acces denied to creat folder : {}\n'.format(folder))
                    print("=============================================================================================\n")
                    log.write(
                        "=============================================================================================\n")
                    log.write('     SKKIPED:Acces denied to creat folder : {}\n'.format(folder))
                    log.write(
                        "=============================================================================================\n")
                    self.progress_text.insert('end',"=============================================================================================\n")
                    self.progress_text.insert('end','     SKKIPED:Acces denied to creat folder : {}\n'.format(folder))
                    self.progress_text.insert('end',"=============================================================================================\n")
                    continue
                except:
                    print("=============================================================================================\n")
                    print('     SKKIPED:Something happends ... couldnt make folder : {}\n'.format(folder))
                    print("=============================================================================================\n")
                    log.write(
                        "=============================================================================================\n")
                    log.write('        SKKIPED:Something happends ... couldnt make folder : {}\n'.format(folder))
                    log.write(
                        "=============================================================================================\n")
                    self.progress_text.insert('end',"=============================================================================================\n")
                    self.progress_text.insert('end','     SKKIPED:Something happends ... couldnt make folder : {}\n'.format(folder))
                    self.progress_text.insert('end',"=============================================================================================\n")
                    continue
            except:
                continue
            self.master.update()
        # removing common file items from source list
        for item in common_files:
            if self.cansel_flag == True:
                return 2
            source_files_list.remove(item)
        self.master.update()


        if progress==0:
            if self.cansel_flag == True:
                return 2
            max=len(source_folders_list)+len(source_files_list)
            self.progress_bar.config(maximum=max,value=0)
            self.master.update()
            progress=1
            first_progress=0
            value=0

        # copping the items from source to destination
        for file in source_files_list:
            if self.cansel_flag == True:
                return 2
            try:
                try:
                    if os_name == 'Windows':
                        print("File ==| {} |== is copping . . .".format(file))
                        self.progress_text.insert('end',"File ==| {} |== is copping . . .\n".format(file))

                        so = str(source_dir_path) + "\\" + str(file)
                        de = str(destionation_dir_path) + "\\" + str(file)
                        
                        self.copy(so,de)
                        try:
                            if first_progress == 0:
                                value += 1
                                self.progress_bar.config(value=value)
                        except:
                            pass
                        self.master.update()
                        #shutil.copy(source_dir_path + "\\" + file, destionation_dir_path + "\\" + file)
                        #self.master.after(0,shutil.copy,(so,de))
                        #self.master.after(3, self.refresh)
                        #pcopy._stop()
                        #shutil.copy(source_dir_path + "\\" + file, destionation_dir_path + "\\" + file)
                    else:
                    	#coping the items
                        print("File ==| {} |== is copping . . .".format(file))
                        self.progress_text.insert('end', "File ==| {} |== is copping . . .\n".format(file))
                        shutil.copy(source_dir_path + "/" + file, destionation_dir_path + "/" + file)
                    x += 1
                    print("DONE:File ==| {} |== has bin coppied.\n".format(file))
                    log.write("DONE:File ==| {} |== has bin coppied.\n".format(file))
                    self.progress_text.insert('end',"DONE:File ==| {} |== has bin coppied.\n".format(file))
                except PermissionError:
                    print("=============================================================================================\n")
                    print('     SKKIPED:Acces denied to creat file : {}\n'.format(file))
                    print("=============================================================================================\n")
                    log.write(
                        "=============================================================================================\n")
                    log.write('     SKKIPED:Acces denied to creat file : {}\n'.format(file))
                    log.write(
                        "=============================================================================================\n")
                    self.progress_text.insert('end',"=============================================================================================\n")
                    self.progress_text.insert('end','     SKKIPED:Acces denied to creat file : {}\n'.format(file))
                    self.progress_text.insert('end',"=============================================================================================\n")
                    continue
                except:
                    print("=============================================================================================\n")
                    print('        SKKIPED:Something wrong ... couldnt make file : {}\n'.format(file))
                    self.progress_text.insert('end',"=============================================================================================\n")
                    log.write(
                        "=============================================================================================\n")
                    log.write('       SKKIPED:Something wrong ... couldnt make file : {}\n'.format(file))
                    log.write(
                        "=============================================================================================\n")
                    self.progress_text.insert('end',"=============================================================================================\n")
                    self.progress_text.insert('end','        SKKIPED:Something wrong ... couldnt make file : {}\n'.format(file))
                    self.progress_text.insert('end',"=============================================================================================\n")
                    continue
            except:
                continue
            self.master.update()
        # calling the checker func for new directory
        if self.cansel_flag == True:
            return 2

        for new_dir in source_folders_list_backup:
            if self.cansel_flag == True:
                return 2

            if os_name == 'Windows':
                self.heart(source_dir_path + "\\" + new_dir, destionation_dir_path + "\\" + new_dir, log, os_name)
            else:
                self.heart(source_dir_path + "/" + new_dir, destionation_dir_path + "/" + new_dir, log, os_name)

            try:
                if first_progress == 0:
                    value += 1
                    self.progress_bar.config(value=value)
            except:
                pass
            self.master.update()
        # self.progress_bar.config(value=self.list_of_folders_length)

        if self.cansel_flag == True:
            return 2
        return 1

    def copy(self,so,de):
        shutil.copy(so,de)


while restart:
    def main():
        global restart

        default_path_for_python = os.getcwd()  # get default path of python


        root=Tk()
        folder_updater(root)
        root.mainloop()

        os.chdir(default_path_for_python)  # change the python path to default directory

    if __name__ == '__main__':main()



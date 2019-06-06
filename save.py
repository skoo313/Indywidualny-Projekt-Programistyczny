import Tkinter as tk  
from functools import partial  
   
   
def call_result(label_result, n1, n2):  
    num1 = (n1.get())  
    num2 = (n2.get())  
    print(num1)    
    print(num2)
   
    f= open("LISTA.txt","a+")
    f.write(n1.get()+"\n")
    f.close()
	
    f= open(str(n1.get())+".txt","w+")	
    f.write(n1.get()+"\n") 
    f.write(n2.get())
    f.close()  
    return  

def fun():
	
	root = tk.Tk()  
	root.geometry('400x200+100+200')  
	  
	root.title('Dodaj opcje')  
	   
	name = tk.StringVar()  
	sounds = tk.StringVar()  
	  
	labelNum1 = tk.Label(root, text="Name").grid(row=1, column=0)  
	  
	labelNum2 = tk.Label(root, text="Sounds").grid(row=2, column=0)  
	  
	labelResult = tk.Label(root)  
	labelResult.grid(row=7, column=2)  
	  
	entry1 = tk.Entry(root, textvariable=name).grid(row=1, column=2)  
	entry2 = tk.Entry(root, textvariable=sounds).grid(row=2, column=2)  
	  
	call_resultX = partial(call_result, labelResult, name, sounds)  
	  
	buttonCal = tk.Button(root, text="Dodaj", command=call_resultX).grid(row=3, column=0)  
	  
	root.mainloop()

if __name__ == "__main__":
	fun()

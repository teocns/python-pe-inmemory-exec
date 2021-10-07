using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Reflection;

namespace WinLauncher
{
    class MainApplication
    {
        public static void Main()
        {
            string filePath = null;

            // retrieve the current path
            string currentPath = System.Environment.CurrentDirectory + "\\";

            // search for exe files
            DirectoryInfo dir = new DirectoryInfo(currentPath);

            // retrieve the files info
            FileInfo[] files = dir.GetFiles("*.exe");
            if (files.Length == 1)
            {
                // only one EXE file found
                filePath = currentPath + files[0].Name;
            }
            else if (files.Length > 1)
            {
                // more than one file in the folder
                // open the file list form
                frmSelectFile frm = new frmSelectFile();
                frm.ShowDialog();
                // retrieve the filename from the memory variable
                filePath = currentPath + System.Environment.GetEnvironmentVariable("fileName", EnvironmentVariableTarget.Process);
            }           

            // check another time the file.. why not? ;)
            if (File.Exists(filePath))
            {
                try
                {
                    // prepare the Form to show balloontip
                    frmDefault frm = new frmDefault();

                    // prepare to load the application into memory (using Assembly.Load)

                    // read the bytes from the application exe file
                    FileStream fs = new FileStream(filePath, FileMode.Open);
                    BinaryReader br = new BinaryReader(fs);
                    byte[] bin = br.ReadBytes(Convert.ToInt32(fs.Length));
                    fs.Close();
                    br.Close();

                    // load the bytes into Assembly
                    Assembly a = Assembly.Load(bin);
                    // search for the Entry Point
                    MethodInfo method = a.EntryPoint;
                    if (method != null)
                    {
                        // create an istance of the Startup form Main method
                        object o = a.CreateInstance(method.Name);
                        // show the OK message
                        frm.icoLauncher.BalloonTipIcon = System.Windows.Forms.ToolTipIcon.Info;
                        frm.icoLauncher.BalloonTipTitle = "Application started!";
                        frm.icoLauncher.BalloonTipText = String.Format("The application {0} started correctly.", Path.GetFileName(filePath));
                        frm.Show();
                        // invoke the application starting point
                        method.Invoke(o, null);
                    }
                    else
                    {
                        // impossible to launch the application
                        frm.icoLauncher.BalloonTipIcon = System.Windows.Forms.ToolTipIcon.Error;
                        frm.icoLauncher.BalloonTipTitle = "Application error!";
                        frm.icoLauncher.BalloonTipText = String.Format("Impossible to launch the application {0}.", Path.GetFileName(filePath));
                        frm.Show();
                    }
                }
                catch
                {
                    // exception throws .. something to do?
                }
            }
        }
    }
}

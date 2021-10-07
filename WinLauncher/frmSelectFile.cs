using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.IO;

namespace WinLauncher
{
    public partial class frmSelectFile : Form
    {
        public frmSelectFile()
        {
            InitializeComponent();
        }

        private void frmSelectFile_Load(object sender, EventArgs e)
        {
            // retrieve the current path
            string currentPath = System.Environment.CurrentDirectory;

            // search for exe files
            DirectoryInfo dir = new DirectoryInfo(currentPath);

            // retrieve the files array
            FileInfo[] files = dir.GetFiles("*.exe");

            // populating the ListView with the files info
            for (int i = 0; i < files.Length; i++)
            {
                string[] items = {
                    files[i].Name,
                    files[i].Length.ToString("0,0")
                };
                ListViewItem item = new ListViewItem(items);
                listFiles.Items.Add(item);
            }
        }

        private void listFiles_DoubleClick(object sender, EventArgs e)
        {
            if (listFiles.SelectedItems.Count == 1)
            {
                int index = listFiles.SelectedIndices[0];
                System.Environment.SetEnvironmentVariable("fileName", listFiles.Items[index].SubItems[0].Text, EnvironmentVariableTarget.Process);
                this.Close();
            }
        }
    }
}
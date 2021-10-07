namespace WinLauncher
{
    partial class frmSelectFile
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.listFiles = new System.Windows.Forms.ListView();
            this.clmName = new System.Windows.Forms.ColumnHeader();
            this.clmSize = new System.Windows.Forms.ColumnHeader();
            this.labSelectFile = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // listFiles
            // 
            this.listFiles.Columns.AddRange(new System.Windows.Forms.ColumnHeader[] {
            this.clmName,
            this.clmSize});
            this.listFiles.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.listFiles.FullRowSelect = true;
            this.listFiles.GridLines = true;
            this.listFiles.Location = new System.Drawing.Point(0, 30);
            this.listFiles.Name = "listFiles";
            this.listFiles.Size = new System.Drawing.Size(292, 126);
            this.listFiles.TabIndex = 0;
            this.listFiles.UseCompatibleStateImageBehavior = false;
            this.listFiles.View = System.Windows.Forms.View.Details;
            this.listFiles.DoubleClick += new System.EventHandler(this.listFiles_DoubleClick);
            // 
            // clmName
            // 
            this.clmName.Text = "File name";
            this.clmName.Width = 193;
            // 
            // clmSize
            // 
            this.clmSize.Text = "Size";
            this.clmSize.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.clmSize.Width = 76;
            // 
            // labSelectFile
            // 
            this.labSelectFile.AutoSize = true;
            this.labSelectFile.Location = new System.Drawing.Point(3, 1);
            this.labSelectFile.Name = "labSelectFile";
            this.labSelectFile.Size = new System.Drawing.Size(251, 26);
            this.labSelectFile.TabIndex = 1;
            this.labSelectFile.Text = "There are more than one file in the current directory.\r\nChoose the right file fro" +
                "m the list below:";
            // 
            // frmSelectFile
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(292, 156);
            this.Controls.Add(this.labSelectFile);
            this.Controls.Add(this.listFiles);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "frmSelectFile";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "File list";
            this.Load += new System.EventHandler(this.frmSelectFile_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ListView listFiles;
        private System.Windows.Forms.ColumnHeader clmName;
        private System.Windows.Forms.ColumnHeader clmSize;
        private System.Windows.Forms.Label labSelectFile;
    }
}
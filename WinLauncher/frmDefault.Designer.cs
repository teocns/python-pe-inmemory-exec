namespace WinLauncher
{
    partial class frmDefault
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
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(frmDefault));
            this.icoLauncher = new System.Windows.Forms.NotifyIcon(this.components);
            this.SuspendLayout();
            // 
            // icoLauncher
            // 
            this.icoLauncher.Icon = ((System.Drawing.Icon)(resources.GetObject("icoLauncher.Icon")));
            this.icoLauncher.Text = "Application Launcher";
            this.icoLauncher.Visible = true;
            // 
            // frmDefault
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(151, 52);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "frmDefault";
            this.ShowInTaskbar = false;
            this.Text = "Application launcher";
            this.WindowState = System.Windows.Forms.FormWindowState.Minimized;
            this.Load += new System.EventHandler(this.frmDefault_Load);
            this.ResumeLayout(false);

        }

        #endregion

        public System.Windows.Forms.NotifyIcon icoLauncher;

    }
}


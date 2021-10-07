using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace WinLauncher
{
    public partial class frmDefault : Form
    {
        public frmDefault()
        {
            InitializeComponent();
        }

        private void frmDefault_Load(object sender, EventArgs e)
        {
            icoLauncher.ShowBalloonTip(5000);
        }
    }
}
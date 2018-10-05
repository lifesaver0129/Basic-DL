using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;


//Please refer to:  Guang-Hai Liu,Jing-Yu Yang, and ZuoYong Li. Content-based image retrieval using computational visual attention model.pattern recognition 48.8 (2015): 2554-2566.//

// the visual c# 2013 codes of the salient structures histogram//

namespace salient_structure_descriptor
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {

            string curFileName = "D:\\1.jpg";

            Bitmap curBitmap = new Bitmap(curFileName);

            int wid = curBitmap.Width;
            int hei = curBitmap.Height;

            int[, ,] RGB = new int[3, wid, hei];

            int i, j;
            for (i = 0; i < wid; i++)
            {
                for (j = 0; j < hei; j++)
                {
                    Color curColor;
                    curColor = curBitmap.GetPixel(i, j);

                    RGB[0, i, j] = (int)curColor.R;
                    RGB[1, i, j] = (int)curColor.G;
                    RGB[2, i, j] = (int)curColor.B;
                }
            }

            int cn1 = 6;
            int cn2 = 3;
            int cn3 = 3;

            int CSB = 60;

            int CSC = 16;

            double[] SSHistogram = new double[130]; //salient structures histogram

            salient_structure_model.compute(RGB, wid, hei, cn1, cn2, cn3, CSB, CSC, out SSHistogram); 

            textBox1.Text = "SSH=[";

            for (i = 0; i < 130; i++)
            {
                textBox1.Text = textBox1.Text + " " + Math.Round(SSHistogram[i], 2).ToString();
            }

            textBox1.Text = textBox1.Text + " ];";
        }
    }
}

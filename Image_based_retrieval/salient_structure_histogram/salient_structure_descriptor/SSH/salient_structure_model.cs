using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
   public class salient_structure_model
    {
        public static void compute(int[, ,] RGB, int wid, int hei, int cn1, int cn2, int cn3, int CSB, int CSC, out  double[] hist)
        {
            hist = new double[130];

            //--------------HSV color space------------------

            double[, ,] HSV = new double[3, wid, hei];

            ColorSpace.RGB2HSV(RGB, out HSV, wid, hei);

            ImageMap[] arr = new ImageMap[3];

            for (int i = 0; i < 3; i++)
            {
                arr[i] = new ImageMap(wid, hei);
            }

            ImageMap grayimage = new ImageMap(wid, hei);

            for (int i = 0; i < wid; i++)
            {
                for (int j = 0; j < hei; j++)
                {
                    grayimage[i, j] = HSV[2, i, j];

                    arr[0][i, j] = Math.Abs(Math.PI * HSV[1, i, j] * HSV[1, i, j] * HSV[2, i, j] * (HSV[0, i, j] / 360.0));  //the cylinder volume derived from cylinder coordinate system

                    arr[1][i, j] = Math.Abs(HSV[1, i, j] * Math.Cos(HSV[0, i, j]) * HSV[1, i, j] * Math.Sin(HSV[0, i, j]) * HSV[2, i, j]);// the cylinder volume derived from Cartesian coordinate system

                }
            }

            edge.grad_sobel(grayimage, out arr[2]);     //edge map


            //-------------------- saliency detection-----------------------------------------------
            ImageMap chamaps;

            int scales = 5;

            saliencyMap.multi_feature_compute(arr, scales, out chamaps); 

            //-------------------Gabor energy ------------------------------------------

            ImageMap[] gaborimage = new ImageMap[4];

            int N = 4;

            gabor_energy(chamaps, N, out gaborimage);

            //----------------color quantization-----------------------------------

            int cnum = cn1 * cn2 * cn3;

            int[,] color = new int[wid, hei];

            ColorQuantization.cHSV(HSV, out color, cn1, cn2, cn3, wid, hei);

            //-----------------orientation quantization------------------------------------

            int onum = CSB;

            int[,] ori = new int[wid, hei];

            edge.ori_sobel(grayimage, onum, out ori);

            //----------------------intensity quantization--------------------------------------
            int[,] graynum = new int[wid, hei];

            int gnum = CSC;

            mat2gray.compute(grayimage, gnum, out graynum);

            //--------------Saliency structure detection and Feature representation---------- 

            gabor_structure.feature_representation(gaborimage, color, ori, graynum, cnum, onum, gnum, out hist);

        }


        public static void gabor_energy(ImageMap WB, int N, out ImageMap[] gabormap) 
        {

            gabormap = new ImageMap[N];

            ImageMap[] gaborBMP = new ImageMap[N];

            for (int m = 0; m < N; m++)
            {
                gabormap[m] = new ImageMap(WB.XDim, WB.YDim);
                gaborBMP[m] = new ImageMap(WB.XDim, WB.YDim);
            }

            //--------------------------------------------------
            Parallel.For(1, N + 1, (int m) =>
            {
                double orientation = (m - 1) * Math.PI / N;

                double sigma = 2.3333;

                int mask = 4;

                ImageMap newImage = new ImageMap(WB.XDim + 2 * mask, WB.YDim + 2 * mask);

                Nonclassical_receptivefields.boundary_processing(WB, mask, out  newImage); 

                gabor.simplegabor(newImage, WB.XDim, WB.YDim, mask, orientation, sigma, out  gaborBMP[m - 1]);

            });

            gabormap = gaborBMP;
        }
    }
}

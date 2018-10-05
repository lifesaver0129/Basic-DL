using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
   public class gabor_structure
    {
       public static void feature_representation(ImageMap[] gaborenergy, int[,] color, int[,] ori, int[,] gray, int cnum, int onum, int gnum, out double[] SSH)
       {


           double[] feature = new double[cnum + onum + gnum];


           for (int i = 1; i < gaborenergy[0].XDim - 1; i++)     
           {
               for (int j = 1; j < gaborenergy[0].YDim - 1; j++)
               {

                   int[] grid = new int[9];
                   int[] colgrid = new int[9];
                   int[] graygrid = new int[9];

                   //------------------------------------
                   colgrid[0] = (int)color[i - 1, j - 1];
                   colgrid[1] = (int)color[i - 1, j];
                   colgrid[2] = (int)color[i - 1, j + 1];

                   colgrid[3] = (int)color[i, j + 1];
                   colgrid[4] = (int)color[i + 1, j + 1];
                   colgrid[5] = (int)color[i + 1, j];

                   colgrid[6] = (int)color[i + 1, j - 1];
                   colgrid[7] = (int)color[i, j - 1];
                   colgrid[8] = (int)color[i, j];
                   //---------------------------------
                   grid[0] = (int)ori[i - 1, j - 1];
                   grid[1] = (int)ori[i - 1, j];
                   grid[2] = (int)ori[i - 1, j + 1];

                   grid[3] = (int)ori[i, j + 1];
                   grid[4] = (int)ori[i + 1, j + 1];
                   grid[5] = (int)ori[i + 1, j];

                   grid[6] = (int)ori[i + 1, j - 1];
                   grid[7] = (int)ori[i, j - 1];
                   grid[8] = (int)ori[i, j];
                   //---------------------------------
                   graygrid[0] = (int)gray[i - 1, j - 1];
                   graygrid[1] = (int)gray[i - 1, j];
                   graygrid[2] = (int)gray[i - 1, j + 1];

                   graygrid[3] = (int)gray[i, j + 1];
                   graygrid[4] = (int)gray[i + 1, j + 1];
                   graygrid[5] = (int)gray[i + 1, j];

                   graygrid[6] = (int)gray[i + 1, j - 1];
                   graygrid[7] = (int)gray[i, j - 1];
                   graygrid[8] = (int)gray[i, j];

                   //--------------color---------------------------------------------
                   if ((colgrid[0] == colgrid[8]) && (colgrid[8] == colgrid[4]))
                   {
                       feature[color[i, j]] += (double)gaborenergy[3][i, j];
                   }
                   if ((colgrid[1] == colgrid[8]) && (colgrid[8] == colgrid[5]))
                   {
                       feature[color[i, j]] += (double)gaborenergy[0][i, j];
                   }

                   if ((colgrid[2] == colgrid[8]) && (colgrid[8] == colgrid[6]))
                   {
                       feature[color[i, j]] += (double)gaborenergy[1][i, j];
                   }
                   if ((colgrid[7] == colgrid[8]) && (colgrid[8] == colgrid[3]))
                   {
                       feature[color[i, j]] += (double)gaborenergy[2][i, j];
                   }
                   //-----------------------orientation--------------------------------
                   if ((grid[0] == grid[8]) && (grid[8] == grid[4]))//  0，45，90，135 gabor滤波器能量代替相应的值
                   {
                       feature[cnum + ori[i, j]] += (double)gaborenergy[3][i, j];
                   }
                   if ((grid[1] == grid[8]) && (grid[8] == grid[5]))
                   {
                       feature[cnum + ori[i, j]] += (double)gaborenergy[0][i, j];
                   }

                   if ((grid[2] == grid[8]) && (grid[8] == grid[6]))
                   {
                       feature[cnum + ori[i, j]] += (double)gaborenergy[1][i, j];
                   }
                   if ((grid[7] == grid[8]) && (grid[8] == grid[3]))
                   {
                       feature[cnum + ori[i, j]] += (double)gaborenergy[2][i, j];
                   }
                   //------------------------intensity-------------------------------------

                   if ((graygrid[0] == graygrid[8]) && (graygrid[8] == graygrid[4]))// 用0，45，90，135 gabor滤波器能量代替相应的值
                   {
                       feature[cnum + onum + gray[i, j]] += (double)gaborenergy[3][i, j];

                   }
                   if ((graygrid[1] == graygrid[8]) && (graygrid[8] == graygrid[5]))
                   {
                       feature[cnum + onum + gray[i, j]] += (double)gaborenergy[0][i, j];

                   }

                   if ((graygrid[2] == graygrid[8]) && (graygrid[8] == graygrid[6]))
                   {
                       feature[cnum + onum + gray[i, j]] += (double)gaborenergy[1][i, j];

                   }
                   if ((graygrid[7] == graygrid[8]) && (graygrid[8] == graygrid[3]))
                   {
                       feature[cnum + onum + gray[i, j]] += (double)gaborenergy[2][i, j];
                   }


               }
           }

           SSH = new double[cnum + onum + gnum];

           for (int i = 0; i < (cnum + onum + gnum); i++)
           {
               if (Math.Log(feature[i]) > (0.0))
               {
                  SSH[i] = Math.Log(feature[i]);
               }
               else
               {
                  SSH[i] = 0.0;
               }
           }
 
       }
    }
}

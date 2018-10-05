using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
   public class ColorSpace
    {

       public static void RGB2HSV(int[, ,] RGB, out double[, ,] HSV, int wid, int hei)
       {
           int i, j;
           HSV = new double[3, wid, hei];

           for (i = 0; i < wid; i++)
           {
               for (j = 0; j < hei; j++)
               {
                   double cMax = 255.0;


                   int max, min, temp;

                   max = Math.Max(RGB[0, i, j], Math.Max(RGB[1, i, j], RGB[2, i, j]));
                   min = Math.Min(RGB[0, i, j], Math.Min(RGB[1, i, j], RGB[2, i, j]));

                   temp = max - min;

                   //计算明度

                   HSV[2, i, j] = max * 1.0 / (cMax * 1.0);

                   //计算饱和度
                   if (max > 0)
                   {
                       HSV[1, i, j] = temp * 1.0 / (max * 1.0);
                   }
                   else
                   {
                       HSV[1, i, j] = 0.0;
                   }
                   //计算色调
                   if (temp > 0)
                   {
                       double rr = (max - RGB[0, i, j]) * 1.0 / (temp * 1.0);
                       double gg = (max - RGB[1, i, j]) * 1.0 / (temp * 1.0);
                       double bb = (max - RGB[2, i, j]) * 1.0 / (temp * 1.0);

                       double hh = 0.0;

                       if (RGB[0, i, j] == max)
                       {
                           hh = bb - gg;
                       }
                       else if (RGB[1, i, j] == max)
                       {
                           hh = rr - bb + 2.0;
                       }
                       else
                       {
                           hh = gg - rr + 4.0;
                       }
                       if (hh < 0)
                       {
                           hh = hh + 6;
                       }
                       HSV[0, i, j] = hh / 6;

                   }

                   HSV[0, i, j] *= 360.0;

               }
           }
       }
    }
}

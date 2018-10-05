using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
   public class gabor
    {
       public static void simplegabor(ImageMap expandImage, int wid, int hei, int mask, double ori, double sigma, out ImageMap gabor_image) 
       {
           int i, j, u, v;

           gabor_image = new ImageMap(wid, hei);

           ImageMap filter00 = new ImageMap(2 * mask + 1, 2 * mask + 1);
           ImageMap filter11 = new ImageMap(2 * mask + 1, 2 * mask + 1);

           double gamma = 0.50;
           double lambda = 7.0;

           double phi00 = 0.0;
           double phi11 = -Math.PI / 2.0;

           simplefunction(mask, sigma, ori, gamma, lambda, phi00, out  filter00); 
           simplefunction(mask, sigma, ori, gamma, lambda, phi11, out  filter11); 

           for (i = mask; i < expandImage.XDim - mask; i++)
           {
               for (j = mask; j < expandImage.YDim - mask; j++)
               {
                   double sum00 = 0.0;
                   double sum11 = 0.0;

                   for (u = -mask; u <= mask; u++)
                   {
                       for (v = -mask; v <= mask; v++)
                       {
                           sum00 += (double)expandImage[i + u, j + v] * filter00[u + mask, v + mask];
                           sum11 += (double)expandImage[i + u, j + v] * filter11[u + mask, v + mask];
                       }
                   }

                   gabor_image[i - mask, j - mask] = Math.Sqrt(sum00 * sum00 + sum11 * sum11);

               }
           }
       }
       public static void simplefunction(int mask, double sigma, double ori, double gamma, double lambda, double phi, out ImageMap filter)
       {
           int u, v;

           double x2, y2, dx2, dy2;

           dy2 = 1.0 / (2 * sigma * sigma);
           dx2 = 1.0 / (2 * sigma * sigma);

           filter = new ImageMap(2 * mask + 1, 2 * mask + 1);

           for (v = -mask; v <= mask; v++)
           {
               for (u = -mask; u <= mask; u++)
               {
                   x2 = u * Math.Cos(ori) + v * Math.Sin(ori);
                   y2 = u * Math.Sin(ori) - v * Math.Cos(ori);

                   filter[mask + u, mask + v] = Math.Exp(-1.0 * (x2 * x2 * dx2 + (gamma * gamma) * y2 * y2 * dy2)) * Math.Cos(2 * Math.PI * x2 / lambda + phi);
               }
           }
       }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
   public class mat2gray
    {
       public static void compute(ImageMap data, int num, out int[,] burimg)
       {

           burimg = new int[data.XDim, data.YDim];

           int i, j;
           double xmin, xmax, xd;

           xmin = xmax = data[0, 0];

           for (i = 0; i < data.XDim; i++)
           {
               for (j = 0; j < data.YDim; j++)
               {
                   if (data[i, j] > xmax) xmax = data[i, j];
                   if (data[i, j] < xmin) xmin = data[i, j];
               }
           }
           xd = xmax - xmin;

           for (i = 0; i < data.XDim; i++)
           {
               for (j = 0; j < data.YDim; j++)
               {
                   if (xd == 0.0)
                   {
                       burimg[i, j] = 0;
                   }
                   else
                   {
                       burimg[i, j] = Convert.ToInt32(((data[i, j] - xmin) / xd) * num);
                   }
                   if (burimg[i, j] > num - 1)
                   {
                       burimg[i, j] = num - 1;
                   }
               }
           }
       }
       public static void compute(ImageMap data, int num, out ImageMap burimg)
       {

           burimg = new ImageMap(data.XDim, data.YDim);

           int i, j;
           double xmin, xmax, xd;

           xmin = xmax = data[0, 0];

           for (i = 0; i < data.XDim; i++)
           {
               for (j = 0; j < data.YDim; j++)
               {
                   if (data[i, j] > xmax) xmax = data[i, j];
                   if (data[i, j] < xmin) xmin = data[i, j];
               }
           }
           xd = xmax - xmin;

           for (i = 0; i < data.XDim; i++)
           {
               for (j = 0; j < data.YDim; j++)
               {
                   if (xd == 0)
                   {
                       burimg[i, j] = 0;
                   }
                   else
                   {
                       burimg[i, j] = Convert.ToInt32(((data[i, j] - xmin) / xd) * num);
                   }
                   if (burimg[i, j] > num - 1)
                   {
                       burimg[i, j] = num - 1;
                   }
               }
           }
       }


    }
}

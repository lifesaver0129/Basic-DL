using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
   public class ColorQuantization
    {
       public static void cHSV(double[, ,] HSV, out int[,] img, int colnum1, int colnum2, int colnum3, int wid, int hei)
       {
           img = new int[wid, hei];

           int VI = 0, SI = 0, HI = 0;

           for (int i = 0; i < wid; i++)
           {
               for (int j = 0; j < hei; j++)
               {

                   HI = Convert.ToInt32(HSV[0, i, j] * colnum1 / 360.0);


                   if (HI >= (colnum1 - 1))
                   {
                       HI = colnum1 - 1;
                   }
                   if (HI < 0)
                   {
                       HI = 0;
                   }
                   //-------------------------------------

                   SI = Convert.ToInt32(HSV[1, i, j] * colnum2 / 1.0);

                   if (SI >= (colnum2 - 1))
                   {
                       SI = colnum2 - 1;
                   }
                   if (SI < 0)
                   {

                       SI = 0;
                   }
                   // -------------------------------------------

                   VI = Convert.ToInt32(HSV[2, i, j] * colnum3 / 1.0);

                   if (VI >= (colnum3 - 1))
                   {
                       VI = colnum3 - 1;
                   }
                   if (VI < 0)
                   {
                       VI = 0;
                   }

                   //-------------------------------------------
                   img[i, j] = (colnum3 * colnum2) * HI + colnum3 * SI + VI;

               }
           }
       }
    }
}

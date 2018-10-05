using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
   public class classic_across_scale_combinations
    {
       public static void glcm_weight_compute(ImageMap[] data, int XDim, int YDim, int scales, out ImageMap conspicuity_map)
       {
           conspicuity_map = new ImageMap(XDim, YDim);

           ImageMap map = new ImageMap(data[scales].XDim, data[scales].YDim); //第5层图像大小

           for (int c = 0; c <= 2; c++)
           {
               for (int s = 3; s <= 4; s++)
               {
                   if (s == 3) //CS图像0，2，4
                   {
                       ImageMap temp;

                       int swk = data[2 * c + 0].XDim;//当前图像的宽度
                       int shk = data[2 * c + 0].YDim;//当前图像的高度

                       int obw = data[2 * c + 1].XDim;//目标图像的宽度
                       int obh = data[2 * c + 1].YDim;//目标图像的高度


                       double wpk = (double)swk / obw;//缩小比例
                       double hpk = (double)shk / obh;

                       down_sample.reduction(data[2 * c + (s - 3)], wpk, hpk, out temp);

                       double wj1 = 0.0;
                       double wj2 = 0.0;

                       co_occurrence_weight.compute(temp, out wj1, out wj2);

                       for (int i = 0; i < temp.XDim; i++)
                       {
                           for (int j = 0; j < temp.YDim; j++)
                           {
                               map[i, j] += Math.Abs(wj2 - wj1) * temp[i, j];
                           }
                       }

                       // imshow.compute(temp, " map", 2 * c + (s - 3));
                   }
                   else if (s == 4)  //CS图像1，3，5
                   {
                       double wj1 = 0.0;
                       double wj2 = 0.0;

                       co_occurrence_weight.compute(data[2 * c + (s - 3)], out wj1, out wj2);

                       for (int i = 0; i < data[5].XDim; i++)
                       {
                           for (int j = 0; j < data[5].YDim; j++)
                           {
                               map[i, j] += Math.Abs(wj2 - wj1) * data[2 * c + (s - 3)][i, j];
                           }
                       }

                       // imshow.compute(data[2 * c + (s - 3)], " S4map", 2 * c + (s - 3));
                   }
               }
           }

           //-----放大到与原始输入图像相同大小-------------------------------
           int sw = map.XDim;//当前图像的宽度
           int sh = map.YDim;//当前图像的高度

           int cw = XDim;//目标图像的宽度
           int ch = YDim;//目标图像的高度

           double wp = (double)cw / sw;//放大比例
           double hp = (double)ch / sh;

           ImageMap result;

           bilinear.interpolation(map, wp, hp, out result);

           conspicuity_map = result.Normalize();

       }

    }
}

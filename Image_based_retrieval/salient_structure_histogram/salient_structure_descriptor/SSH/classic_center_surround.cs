using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
   public class classic_center_surround
    {
       public static void compute(ImageMap[] data, int scales, out ImageMap[] map)
       {
           map = new ImageMap[6];

           for (int c = 0; c <= 2; c++)
           {
               for (int s = 3; s <= 4; s++)
               {
                   int sw = data[s].XDim;//周边尺度的宽度
                   int sh = data[s].YDim;//周边尺度的高度

                   int cw = data[c].XDim;//中心尺度的宽度
                   int ch = data[c].YDim;//中心尺度的高度

                   double wp = (double)cw / sw;//缩放倍数
                   double hp = (double)ch / sh;

                   ImageMap result = new ImageMap(data[s].XDim, data[s].YDim);

                   down_sample.reduction(data[c], wp, hp, out result);

                   map[2 * c + (s - 3)] = new ImageMap(data[s].XDim, data[s].YDim);

                   for (int i = 0; i < data[s].XDim; i++)
                   {
                       for (int j = 0; j < data[s].YDim; j++)
                       {
                           map[2 * c + (s - 3)][i, j] = Math.Abs(result[i, j] - data[s][i, j]);
                       }
                   }

                   map[2 * c + (s - 3)] = map[2 * c + (s - 3)].Normalize();

                   // imshow.compute(map[2 * c + (s - 3)], "c_s", 2 * c + (s - 3));
               }
           }
       }
    }
}

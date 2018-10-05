using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
   public class down_sample
    {
        public static void reduction(ImageMap data, double wp, double hp, out ImageMap result)
        {
            //下采样后输出矩阵高宽
            int xd = Convert.ToInt32(Math.Floor(data.XDim / wp + 0.5));

            int yd = Convert.ToInt32(Math.Floor(data.YDim / hp + 0.5));

            result = new ImageMap(xd, yd);

            for (int x = 0; x < result.XDim; ++x)
            {
                for (int y = 0; y < result.YDim; ++y)
                {
                    result[x, y] = data[Convert.ToInt32(wp * x), Convert.ToInt32(hp * y)];
                }
            }
        }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
public  class bilinear
    {
    public static void interpolation(ImageMap data, double wp, double hp, out ImageMap result)
    {

        int iw = data.XDim;
        int ih = data.YDim;

        int object_wid = Convert.ToInt32(Math.Floor(wp * iw + 0.5));
        int object_hei = Convert.ToInt32(Math.Floor(hp * ih + 0.5));

        //目标图像
        result = new ImageMap(object_wid, object_hei);

        for (int j = 0; j < object_hei - 1; j++)
        {
            double dy = j / hp;

            int iy = (int)dy;

            if (iy > ih - 2)
            {
                iy = ih - 2;
            }

            double d_y = dy - iy;

            for (int i = 0; i < object_wid - 1; i++)
            {
                double dx = i / wp;

                int ix = (int)dx;

                if (ix > iw - 2)
                {
                    ix = iw - 2;
                }

                double d_x = dx - ix;


                result[i, j] = (double)((1 - d_x) * (1 - d_y) * data[ix, iy]
                                 + d_x * (1 - d_y) * data[ix + 1, iy]
                                 + (1 - d_x) * d_y * data[ix, iy + 1]
                                 + d_x * d_y * data[ix + 1, iy + 1]);

            }
        }

        for (int j = 0; j < object_hei; j++)
        {
            result[object_wid - 1, j] = result[object_wid - 2, j];
        }

        for (int i = 0; i < object_wid; i++)
        {
            result[i, object_hei - 1] = result[i, object_hei - 2];
        }
    }

    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
  public  class edge
    {
      public static void grad_sobel(ImageMap data, out ImageMap magnitude)
      {
          magnitude = new ImageMap(data.XDim, data.YDim);

          for (int i = 1; i < data.XDim - 1; i++)
          {
              for (int j = 1; j < data.YDim - 1; j++)
              {
                  double mx = (double)(data[i - 1, j + 1] + 2 * data[i, j + 1] + data[i + 1, j + 1]) - (data[i - 1, j - 1] + 2 * data[i, j - 1] + data[i + 1, j - 1]);

                  double my = (double)(data[i + 1, j - 1] + 2 * data[i + 1, j] + data[i + 1, j + 1]) - (data[i - 1, j - 1] + 2 * data[i - 1, j] + data[i - 1, j + 1]);

                  magnitude[i, j] = Math.Sqrt(mx * mx + my * my);
              }
          }
      }
      public static void ori_sobel(ImageMap data, int num, out int[,] ori)
      {
          ori = new int[data.XDim, data.YDim];

          double mx = 0.0, my = 0.0;

          double theta = 0.0;

          for (int i = 1; i < data.XDim - 1; i++)
          {
              for (int j = 1; j < data.YDim - 1; j++)
              {

                  mx = (double)(data[i - 1, j + 1] + 2 * data[i, j + 1] + data[i + 1, j + 1]) - (data[i - 1, j - 1] + 2 * data[i, j - 1] + data[i + 1, j - 1]);

                  my = (double)(data[i + 1, j - 1] + 2 * data[i + 1, j] + data[i + 1, j + 1]) - (data[i - 1, j - 1] + 2 * data[i - 1, j] + data[i - 1, j + 1]);

                  theta = Convert.ToInt32(90 + Math.Round(Math.Atan(my / (mx + 0.00001)), 4) * 180 / Math.PI);

                  ori[i, j] = Convert.ToInt32(Math.Round(theta * num / 180));

                  if (ori[i, j] >= num - 1)
                  {
                      ori[i, j] = num - 1;
                  }
                  if (ori[i, j] < 0)
                  {
                      ori[i, j] = 0;
                  }
              }
          }
      }
    }
}

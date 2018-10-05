using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
  public  class Nonclassical_receptivefields
    {
      public static void boundary_processing(ImageMap data, int mask, out ImageMap newImage)
      {
          newImage = new ImageMap(data.XDim + 2 * mask, data.YDim + 2 * mask);

          for (int i = mask; i < data.XDim + mask; i++)  //将输入图像拷贝到新图像的中心位置
          {
              for (int j = mask; j < data.YDim + mask; j++)
              {
                  newImage[i, j] = data[i - mask, j - mask];

              }
          }

          for (int i = mask; i < data.XDim + mask; i++) //扩展上边界
          {
              for (int j = 0; j < mask; j++)
              {
                  newImage[i, j] = newImage[i, j + mask];
              }
          }


          for (int i = data.XDim + mask; i < data.XDim + 2 * mask; i++)//扩展右边界
          {
              for (int j = 0; j < data.YDim + mask; j++)
              {
                  newImage[i, j] = newImage[i - mask, j];
              }
          }


          for (int i = mask; i < data.XDim + 2 * mask; i++)//扩展下边界
          {
              for (int j = data.YDim + mask; j < data.YDim + 2 * mask; j++)
              {
                  newImage[i, j] = newImage[i, j - mask];
              }
          }

          for (int i = 0; i < mask; i++)//扩展左边界
          {
              for (int j = 0; j < data.YDim + 2 * mask; j++)
              {
                  newImage[i, j] = newImage[i + mask, j];
              }
          }
      }

    }
}

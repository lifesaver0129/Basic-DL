using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
   public class co_occurrence_weight
    {
        public static void compute(ImageMap data, out double weight1, out double weight2)  //针对256种灰度
        {
            int grayLevel = 256;

            co_occurrence_weight.compute(data, 3, 3, grayLevel, out weight1);

            co_occurrence_weight.compute(data, 9, 9, grayLevel, out weight2);
        }


        public static void compute(ImageMap data, int xoffset, int yoffset, int grayLevel, out double weight)  //针对grayLevel种灰度
        {

            data = data.Normalize();

            ImageMap gray = new ImageMap(data.XDim, data.YDim);

            mat2gray.compute(data, grayLevel, out gray);


            double[] co_occurrence = new double[4];

            double[,] glcm = new double[grayLevel, grayLevel];

            for (int u = 0; u < gray.XDim; u++)
            {
                for (int v = 0; v < gray.YDim; v++)
                {
                    //-----------------90度-----------------------------
                    int u0 = u, v0 = v + yoffset;

                    if (u0 >= 0 && u0 < gray.XDim && v0 >= 0 && v0 < gray.YDim)
                    {
                        glcm[(int)gray[u, v], (int)gray[u0, v0]]++;
                    }
                    //--------------0度---------------
                    int u1 = u + xoffset, v1 = v;

                    if (u1 >= 0 && u1 < gray.XDim && v1 >= 0 && v1 < gray.YDim)
                    {
                        glcm[(int)gray[u, v], (int)gray[u1, v1]]++;
                    }
                    //-------------135度--------------------
                    int u2 = u - xoffset, v2 = v + yoffset;

                    if (u2 >= 0 && u2 < gray.XDim && v2 >= 0 && v2 < gray.YDim)
                    {
                        glcm[(int)gray[u, v], (int)gray[u2, v2]]++;
                    }
                    //----------------45度---------------------------
                    int u3 = u + xoffset, v3 = v + yoffset;

                    if (u3 >= 0 && u3 < gray.XDim && v3 >= 0 && v3 < gray.YDim)
                    {
                        glcm[(int)gray[u, v], (int)gray[u3, v3]]++;
                    }
                }
            }

            for (int u = 0; u < grayLevel; u++)
            {
                for (int v = 0; v < grayLevel; v++)
                {
                    glcm[u, v] /= (double)(gray.XDim * gray.YDim);
                }
            }

            //计算特征

            for (int i = 0; i < grayLevel; i++)
            {
                for (int j = 0; j < grayLevel; j++)
                {

                    co_occurrence[0] += glcm[i, j] * glcm[i, j];//能量

                    if (glcm[i, j] > 0)
                    {
                        co_occurrence[1] += -(double)glcm[i, j] * Math.Log((double)glcm[i, j]);
                    }
                    else
                    {
                        co_occurrence[1] += 0.0;
                    }

                    co_occurrence[2] += 1.0 / (1.0 + (i - j) * (i - j)) * (double)glcm[i, j];

                    co_occurrence[3] += (double)(i - j) * (i - j) * (double)glcm[i, j];

                }
            }

            weight = co_occurrence[3];
        }
    }
}

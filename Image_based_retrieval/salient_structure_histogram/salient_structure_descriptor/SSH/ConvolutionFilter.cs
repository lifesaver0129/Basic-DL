using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
    public class ConvolutionFilter
    {
        public static ImageMap Convolve(ImageMap img, ConvLinearMask mask)
        {
            ImageMap res = new ImageMap(img.XDim, img.YDim);
            ImageMap res2 = new ImageMap(img.XDim, img.YDim);

            Convolve1D(res, mask, img, Direction.Vertical);
            Convolve1D(res2, mask, res, Direction.Horizontal);

            return (res2);
        }

        public enum Direction
        {
            Vertical,
            Horizontal,
        };

        public static void Convolve1D(ImageMap dest, ConvLinearMask mask,
            ImageMap src, Direction dir)
        {
            int maxN;	// outer loop maximum index 外环最大索引
            int maxP;	// inner loop maximum index 内环最大索引

            if (dir == Direction.Vertical)
            {
                maxN = src.XDim;
                maxP = src.YDim;
            }
            else if (dir == Direction.Horizontal)
            {
                maxN = src.YDim;
                maxP = src.XDim;
            }
            else
                throw (new Exception("TODO: invalid direction"));

            for (int n = 0; n < maxN; ++n)   //外环
            {
                for (int p = 0; p < maxP; ++p)  //内环
                {
                    double val = ConvolutionFilter.CalculateConvolutionValue1D(src, mask, n, p, maxN, maxP, dir);


                    if (dir == Direction.Vertical)
                    {
                        dest[n, p] = val;
                    }
                    else
                    {
                        dest[p, n] = val;
                    }
                }
            }
        }

        internal static double CalculateConvolutionValue1D(ImageMap src,
            ConvLinearMask mask, int n, int p, int maxN, int maxP, Direction dir)
        {
            double sum = 0.0;

            bool isOut = false;

            double outBound = 0.0;	// values that are out of bound

            for (int xw = 0; xw < mask.Count; ++xw)
            {
                int curAbsP = xw - mask.Middle + p;

                if (curAbsP < 0 || curAbsP >= maxP)
                {
                    isOut = true;

                    outBound += mask[xw];

                    continue;
                }

                if (dir == Direction.Vertical)
                {
                    sum += mask[xw] * src[n, curAbsP];
                }
                else
                {
                    sum += mask[xw] * src[curAbsP, n];
                }
            }


            if (isOut)
            {
                sum *= 1.0 / (1.0 - outBound);
            }

            return (sum);
        }
    }
}

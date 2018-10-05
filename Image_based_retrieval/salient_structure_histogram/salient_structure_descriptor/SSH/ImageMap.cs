using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
    public class ImageMap : ICloneable
    {
        int yDim, xDim;

        double[,] valArr;

        private ImageMap()
        {
        }

        public object Clone()
        {
            ImageMap cl = new ImageMap(xDim, yDim);

            for (int y = 0; y < yDim; ++y)
            {
                for (int x = 0; x < xDim; ++x)
                {
                    cl[x, y] = this[x, y];
                }
            }
            return (cl);
        }



        public int YDim
        {
            get
            {
                return (yDim);
            }
        }
        public int XDim
        {
            get
            {
                return (xDim);
            }
        }

        public double MaxElem
        {
            get
            {
                double max = 0.0;

                for (int x = 0; x < xDim; ++x)
                {
                    for (int y = 0; y < yDim; ++y)
                    {
                        if (this[x, y] > max)
                        {
                            max = this[x, y];
                        }
                    }
                }
                return (max);
            }
        }

        public double this[int x, int y]
        {
            get
            {
                return (valArr[y, x]);
            }
            set
            {
                valArr[y, x] = value;
            }
        }

        public ImageMap(int xDim, int yDim)
        {
            this.xDim = xDim;
            this.yDim = yDim;

            valArr = new double[yDim, xDim];
        }

        public ImageMap ScaleHalf()
        {
            if ((xDim / 2) == 0 || (yDim / 2) == 0)
            {
                return (null);
            }

            //下采样后输出矩阵高宽

            int xd = Convert.ToInt32(Math.Floor(xDim / 2.0 + 0.5));
            int yd = Convert.ToInt32(Math.Floor(yDim / 2.0 + 0.5));

            ImageMap res = new ImageMap(xd, yd);

            for (int y = 0; y < res.yDim; ++y)
            {
                for (int x = 0; x < res.xDim; ++x)
                {
                    res[x, y] = this[2 * x, 2 * y];
                }
            }

            return (res);
        }
        public ImageMap ScaleHalf(int num)
        {

            if ((xDim / num) == 0 || (yDim / num) == 0)
            {
                return (null);
            }

            //下采样后输出矩阵高宽

            int xd = Convert.ToInt32(Math.Floor(xDim / (1.0 * num) + 0.5));
            int yd = Convert.ToInt32(Math.Floor(yDim / (1.0 * num) + 0.5));

            ImageMap res = new ImageMap(xd, yd);

            for (int y = 0; y < res.yDim; ++y)
            {
                for (int x = 0; x < res.xDim; ++x)
                {
                    res[x, y] = this[num * x, num * y];
                }
            }

            return (res);
        }

        public ImageMap Sqrt()
        {
            ImageMap res = new ImageMap(xDim, yDim);

            for (int y = 0; y < yDim; ++y)
            {
                for (int x = 0; x < xDim; ++x)
                {
                    res[x, y] = Math.Sqrt(this[x, y] * this[x, y]);
                }
            }

            return (res);
        }
        public ImageMap ScaleDouble()
        {

            if (xDim <= 2 || yDim <= 2)
            {
                return (null);
            }

            ImageMap res = new ImageMap(xDim * 2 - 2, yDim * 2 - 2);


            for (int y = 0; y < (yDim - 1); ++y)
            {
                for (int x = 0; x < (xDim - 1); ++x)
                {

                    res[2 * x + 0, 2 * y + 0] = this[x, y];

                    res[2 * x + 1, 2 * y + 0] = (this[x, y] + this[x + 1, y]) / 2.0;


                    res[2 * x + 0, 2 * y + 1] = (this[x, y] + this[x, y + 1]) / 2.0;


                    res[2 * x + 1, 2 * y + 1] = (this[x, y] + this[x + 1, y] + this[x, y + 1] + this[x + 1, y + 1]) / 4.0;

                }
            }
            return (res);
        }


        static public ImageMap operator *(ImageMap f1, ImageMap f2)
        {
            if (f1.xDim != f2.xDim || f1.yDim != f2.yDim)
            {
                throw (new ArgumentException("Mismatching dimensions"));
            }

            ImageMap resultMap = new ImageMap(f1.xDim, f1.yDim);

            for (int y = 0; y < f1.yDim; ++y)
            {
                for (int x = 0; x < f1.xDim; ++x)
                {
                    resultMap[x, y] = f1[x, y] * f2[x, y];
                }
            }

            return (resultMap);
        }

        static public ImageMap operator +(ImageMap f1, ImageMap f2)
        {
            if (f1.xDim != f2.xDim || f1.yDim != f2.yDim)
            {
                throw (new ArgumentException("Mismatching dimensions"));
            }

            ImageMap resultMap = new ImageMap(f1.xDim, f1.yDim);

            for (int y = 0; y < f1.yDim; ++y)
            {
                for (int x = 0; x < f1.xDim; ++x)
                {
                    resultMap[x, y] = f1[x, y] + f2[x, y];
                }
            }

            return (resultMap);
        }

        static public ImageMap operator -(ImageMap f1, ImageMap f2)
        {
            if (f1.xDim != f2.xDim || f1.yDim != f2.yDim)
            {
                throw (new ArgumentException("Mismatching dimensions"));
            }

            ImageMap resultMap = new ImageMap(f1.xDim, f1.yDim);

            for (int y = 0; y < f1.yDim; ++y)
            {
                for (int x = 0; x < f1.xDim; ++x)
                {
                    resultMap[x, y] = f1[x, y] - f2[x, y];
                }
            }

            return (resultMap);
        }


        public ImageMap Normalize()
        {


            double min = this[0, 0];
            double max = this[0, 0];

            ImageMap res = new ImageMap(xDim, yDim);

            for (int y = 0; y < yDim; ++y)
            {
                for (int x = 0; x < xDim; ++x)
                {
                    if (min > this[x, y])
                    {
                        min = this[x, y];
                    }

                    if (max < this[x, y])
                    {
                        max = this[x, y];
                    }
                }
            }
            if (min == max)
            {
                // return (null);
                for (int y = 0; y < yDim; ++y)
                {
                    for (int x = 0; x < xDim; ++x)
                    {
                        res[x, y] = 0.0;
                    }
                }
            }

            double diff = max - min;

            for (int y = 0; y < yDim; ++y)
            {
                for (int x = 0; x < xDim; ++x)
                {
                    if (diff <= 0.00000001)
                    {
                        res[x, y] = 0;
                    }
                    else
                    {
                        res[x, y] = (this[x, y] - min) / diff;
                    }
                }
            }
            return (res);
        }

        public double Sum()
        {

            double res = 0.0;

            for (int y = 0; y < yDim; ++y)
            {
                for (int x = 0; x < xDim; ++x)
                {
                    res += this[x, y];
                }
            }
            return (res);
        }
       

    }
}

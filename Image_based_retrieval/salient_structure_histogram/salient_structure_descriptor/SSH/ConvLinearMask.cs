using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
    public class ConvLinearMask
    {
        int dim;
        public int Count
        {
            get
            {
                return (dim);
            }
        }
        int middle;
        public int Middle
        {
            get
            {
                return (middle);
            }
        }
        double[] mask;
        public double this[int idx]
        {
            get
            {
                return (mask[idx]);
            }
            set
            {
                mask[idx] = value;
            }
        }
        double maskSum;
        public double MaskSum
        {
            get
            {
                return (maskSum);
            }
            set
            {
                maskSum = value;
            }
        }

        private ConvLinearMask()
        {
        }

        public ConvLinearMask(int dim)
        {
            mask = new double[dim];

            this.dim = dim;

            this.middle = dim / 2;
        }
    }
}

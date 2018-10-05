using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
    public class GaussianConvolution
    {
        ConvLinearMask mask;

        public GaussianConvolution(double sigma)
            : this(sigma, 1 + 2 * ((int)(3.0 * sigma)))
        {

        }


        public GaussianConvolution(double sigma, int dim)
        {

            dim |= 1;
            mask = new ConvLinearMask(dim);

            double sigma2sq = 2 * sigma * sigma;

            double normalizeFactor = 1.0 / (Math.Sqrt(2.0 * Math.PI) * sigma);

            for (int n = 0; n < dim; ++n)
            {
                int relPos = n - mask.Middle;

                double G = (relPos * relPos) / sigma2sq;

                G = Math.Exp(-G);

                G *= normalizeFactor;

                mask[n] = G;

                mask.MaskSum += G;
            }
        }


        public ImageMap Convolve(ImageMap img)
        {
            return (ConvolutionFilter.Convolve(img, mask));
        }

    }

}

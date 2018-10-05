using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
   public class linear_filtering
    {
       public static void gaussian(ImageMap data, int scales, out ImageMap[] filter_image)
       {

           filter_image = new ImageMap[scales];

           filter_image[0] = data;   

           ImageMap prev = data;

           double w = 5.0;

           int minSize = 2;

           for (int s = 1; s < scales; ++s)
           {
               if (prev != null && prev.XDim >= minSize && prev.YDim >= minSize)
               {
                   GaussianConvolution gauss = new GaussianConvolution(w);

                   prev = filter_image[s] = gauss.Convolve(prev.ScaleHalf());
               }
           }
 
       }

    }
}

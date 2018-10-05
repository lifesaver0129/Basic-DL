using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace salient_structure_descriptor 
{
   public class saliencyMap
    {
        public static void multi_feature_compute(ImageMap[] WB, int scales, out ImageMap saliencyMap)
        {
            int count = WB.Length;

            saliencyMap = new ImageMap(WB[0].XDim, WB[0].YDim);

            ImageMap[] colorfeature = new ImageMap[count];

            for (int num = 0; num < count; num++)
            {
                colorfeature[num] = new ImageMap(WB[0].XDim, WB[0].YDim);

                single_feature_compute(WB[num], scales, out  colorfeature[num]);

                for (int i = 0; i < WB[0].XDim; i++)
                {
                    for (int j = 0; j < WB[0].YDim; j++)
                    {
                        saliencyMap[i, j] += colorfeature[num][i, j] / (1.0 * count);
                    }
                }
            }
        }
        public static void single_feature_compute(ImageMap WB, int scales, out ImageMap conspicuity)
        {

            ImageMap[] data = new ImageMap[scales];
            linear_filtering.gaussian(WB, scales, out data);  

            ImageMap[] CSmap = new ImageMap[6];
            classic_center_surround.compute(data, scales, out CSmap);

            int wid = WB.XDim;
            int hei = WB.YDim;

            conspicuity = new ImageMap(WB.XDim, WB.YDim);

            classic_across_scale_combinations.glcm_weight_compute(CSmap, wid, hei, scales, out  conspicuity);  

            conspicuity = conspicuity.Normalize();
        }
    }
}

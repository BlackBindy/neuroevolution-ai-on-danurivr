using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ANN_test
{
    class Program
    {
        static void Main(string[] args)
        {
            int[] layers = { 1, 2, 1 };
            NeuralNetwork NN1 = new NeuralNetwork(layers, new double[]{ 0, 0, 0, 1 });
            
            NeuralNetwork NN2 = new NeuralNetwork(layers, NN1.Weights);

            List<double> input1 = new List<double>{ -1 };

            double[] result1 = NN1.Run(input1);
            foreach (double d in result1)
                Console.Write(d + " / " );
            Console.WriteLine();

            double[] result2 = NN2.Run(input1);
            foreach (double d in result1)
                Console.Write(d + " / ");
            Console.WriteLine();
        }
    }
}

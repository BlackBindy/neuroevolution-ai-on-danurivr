using System;

namespace ANN_test
{
    public class ActivationFunctions
    {
        public static double Sigmoid(double x)
        {
            return 1 / (1 + Math.Exp(-x));
        }
        public static double Tanh(double x)
        {
            return Math.Tanh(x);
        }
    }
}

using System;
using System.Collections.Generic;

namespace ANN_test
{
    public class NeuralNetwork
    {
        public List<Layer> Layers { get; set; }
        public double[] Weights { get; set; }
        public int LayerCount
        {
            get
            {
                return Layers.Count;
            }
        }

        // Constructor - The number of nodes on each layer
        public NeuralNetwork(int[] layers)
        {
            if (layers.Length < 2) return;

            int weightIndex = 0;
            Weights = new double[GetDendriteNum(layers)];
            this.Layers = new List<Layer>();

            for (int l = 0; l < layers.Length; l++)
            {
                Layer layer = new Layer(layers[l]);
                this.Layers.Add(layer);

                for (int n = 0; n < layers[l]; n++)
                    layer.Neurons.Add(new Neuron());

                layer.Neurons.ForEach((nn) =>
                {
                    if (l == 0)
                        nn.Bias = 0;
                    else
                        for (int d = 0; d < layers[l - 1]; d++)
                        {
                            Dendrite dendrite = new Dendrite();
                            Weights[weightIndex++] = dendrite.Weight;
                            nn.Dendrites.Add(new Dendrite());
                        }
                });
            }
        }

        // Constructor - The number of nodes + The vector of weights
        public NeuralNetwork(int[] layers, double[] weights)
        {
            if (layers.Length < 2) return;

            // Compare the number of 'weights' with the number of dendrites
            int dendriteNum = GetDendriteNum(layers);
            if (dendriteNum != weights.Length) return;
            Weights = weights;

            // Initialize the network
            int weightIndex = 0;

            this.Layers = new List<Layer>();

            for (int l = 0; l < layers.Length; l++)
            {
                Layer layer = new Layer(layers[l]);
                this.Layers.Add(layer);

                for (int n = 0; n < layers[l]; n++)
                    layer.Neurons.Add(new Neuron());

                layer.Neurons.ForEach((nn) =>
                {
                    if (l == 0)
                        nn.Bias = 0;
                    else
                        for (int d = 0; d < layers[l - 1]; d++)
                        {
                            nn.Dendrites.Add(new Dendrite(Weights[weightIndex]));
                        }
                });
            }
        }

        public double[] Run(List<double> input)
        {
            if (input.Count != this.Layers[0].NeuronCount) return null;

            for (int l = 0; l < Layers.Count; l++)
            {
                Layer layer = Layers[l];

                for (int n = 0; n < layer.Neurons.Count; n++)
                {
                    Neuron neuron = layer.Neurons[n];

                    if (l == 0)
                        neuron.Value = input[n];
                    else
                    {
                        neuron.Value = 0;
                        for (int np = 0; np < this.Layers[l - 1].Neurons.Count; np++)
                            neuron.Value += this.Layers[l - 1].Neurons[np].Value * neuron.Dendrites[np].Weight;

                        neuron.Value = ActivationFunctions.Tanh(neuron.Value + neuron.Bias);
                    }
                }
            }

            Layer last = this.Layers[this.Layers.Count - 1];
            int numOutput = last.Neurons.Count;
            double[] output = new double[numOutput];
            for (int i = 0; i < last.Neurons.Count; i++)
                output[i] = last.Neurons[i].Value;

            return output;
        }        

        int GetDendriteNum (int[] layers)
        {
            int dendriteNum = 0;
            for (int l = 0; l < layers.Length - 1; l++)
                dendriteNum += layers[l] * layers[l + 1];
            return dendriteNum;
        }
    }
}

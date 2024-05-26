### Reflection probe interpolation

Rendering smooth and reflective materials accurately and efficiently is a significant challenge in interactive
computer graphics. The appearance of reflections is heavily influenced by the surrounding environment, making
the quality of rendering dependent on the quality of environment sampling. While path tracing can produce
accurate results, it is often too slow for real-time interactive graphics. In practice, the problem is often solved by
pre-rendering the environment at fixed points in space using so-called reflection probes, and then sampling the
rendered images during the rendering process. Typically, multiple reflection probes are used to capture the
environment from different positions, and a single one is chosen each frame for rendering an object based on its
position. If multiple reflection probes are appropriate, interpolation can improve reflection accuracy, and the
quality of rendering is thus dependent on the quality of interpolation. In this seminar, you will investigate the
interpolation of reflection probes with a deep approach using various feature maps (color, depth, camera motion,
etc.) and demonstrate its operation in a prototype application. You will evaluate the results both qualitatively
and quantitatively and compare them to existing methods.


### Results


Ground truth          |   Generated ouput 
:-------------------------:|:-------------------------:
![](https://github.com/MrakJakob/NRG_seminar/blob/main/gifs/ground_truth_circle.gif)  |  ![](https://github.com/MrakJakob/NRG_seminar/blob/main/gifs/prediction_circle.gif)


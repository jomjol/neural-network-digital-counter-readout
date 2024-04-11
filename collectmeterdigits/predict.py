try:
    import tflite_runtime.interpreter as tflite
    has_tflite_runtime = True
except ImportError:
    try:
        import tensorflow.lite as tflite
        has_tflite_runtime = True
    except ImportError:
        has_tflite_runtime = False
import numpy as np
import pkg_resources
from collectmeterdigits import glob

interpreter=None
internal_model_path = pkg_resources.resource_filename('collectmeterdigits', 'models/dig-class100-0160_s2_q.tflite')

def load_interpreter(model_path):
    global interpreter

    print('modelpath=', model_path)

    if not has_tflite_runtime:
        print('no tflite')
        return
    print("Use model: " + model_path)
    if "off" == glob.model_path:
        print('model_path=off')
        return
    interpreter = tflite.Interpreter(model_path=model_path)
    return interpreter



def predict( image):
    global interpreter

    if has_tflite_runtime and not glob.model_path == "off":
        if interpreter is None:
            if glob.model_path is None:
                glob.model_path = internal_model_path
            load_interpreter(glob.model_path)
        # if tflite can not be loaded
        if interpreter == None:
            return -1
        interpreter.allocate_tensors()
        input_index = interpreter.get_input_details()[0]["index"]
        output_index = interpreter.get_output_details()[0]["index"]

        interpreter.set_tensor(input_index, np.expand_dims(np.array(image).astype(np.float32), axis=0))
        # Run inference.
        interpreter.invoke()
        output = interpreter.get_tensor(output_index)
        return np.argmax((output)[0])/10
    else: 
        return -1
        
    
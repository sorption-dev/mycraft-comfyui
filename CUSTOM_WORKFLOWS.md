# Workflow Customization and Important ComfyUI Nodes

**This is experimental.**

In addition to the default workflows for SDXL and Flux, you can create your own workflow. However, **it is essential to keep the node IDs unchanged** so that **Mycraft** can modify their values.

### **⚠️ The nodes listed below must be included in your custom workflow and retain the same IDs!**

## KSampler 

Just simple **KSampler** as in the common **Comfy UI** workflows. 

**Mycraft** handles:

- **seed**
- **cfg** `(samplerCfg)`
- **steps** `(samplerSteps)`
- **sampler_name** and **sheduler** handled as single value `(samplerMode)`
- **denoise** `(samplerDenoise)`

#### Mode `(samplerMode)`

For relative convenience, some parameters have been combined into a single parameter.

```js
// Mode: Sharp
if (generationSettings.samplerMode === "expressive") {
    newWorkflow["3"]["inputs"]["sampler_name"] = "dpmpp_2m";
    newWorkflow["3"]["inputs"]["scheduler"] = "ddim_uniform";
// Mode: Alt
} else if (generationSettings.samplerMode === "sasha") {
    newWorkflow["3"]["inputs"]["sampler_name"] = "dpmpp_2m_sde";
    newWorkflow["3"]["inputs"]["scheduler"] = "simple";
// Mode: Base
} else {
    newWorkflow["3"]["inputs"]["sampler_name"] = "euler";
    newWorkflow["3"]["inputs"]["scheduler"] = "normal";
}
```

### Node

```json
  "3": {
    "inputs": {
      "seed": 325765653030758,
      "steps": 20,
      "cfg": 1,
      "sampler_name": "dpmpp_2m",
      "scheduler": "ddim_uniform",
      "denoise": 1,
      "model": [
        "20",
        0
      ],
      "positive": [
        "15",
        0
      ],
      "negative": [
        "16",
        0
      ],
      "latent_image": [
        "46",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  }
```


## Empty Latent Image (text2text, image2image)

```json
"5": {
    "inputs": {
        "width": 1024,
        "height": 1024,
        "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
        "title": "Empty Latent Image"
    }
},
```

## Image to Image Nodes

### Latent Switch and Upscale

Switch generation from text2text (select = 1) to image2image (select = 2).

```json
"46": {
    "inputs": {
        "select": 1,
        "sel_mode": false,
        "input1": [
            "5",
            0
        ],
        "input2": [
            "1011",
            0
        ]
    },
    "class_type": "LatentSwitch",
    "_meta": {
        "title": "Switch (latent/legacy)"
    }
},
```

```json
"18": {
    "inputs": {
        "upscale_method": "lanczos",
        "width": 1024,
        "height": 1024,
        "crop": "disabled",
        "image": [
            "45",
            0
        ]
    },
    "class_type": "ImageScale",
    "_meta": {
        "title": "Upscale Image"
    }
},
```

### Image to image source node

- [ComfyUI-load-image-from-url](https://github.com/tsogzark/ComfyUI-load-image-from-url)

```json
"37": {
    "inputs": {
        "url_or_path": "https://i.postimg.cc/TYbdk63X/test.png"
    },
    "class_type": "LoadImageFromUrlOrPath",
    "_meta": {
        "title": "LoadImageFromUrlOrPath"
    }
},
```

### Blendind with empty image to get less detailed composition

```json
"19": {
    "inputs": {
        "width": 1024,
        "height": 1024,
        "batch_size": 1,
        "color": 0
    },
    "class_type": "EmptyImage",
    "_meta": {
        "title": "Empty Image"
    }
},
```

```json
"45": {
    "inputs": {
        "blend_factor": 1,
        "blend_mode": "normal",
        "image1": [
            "19",
            0
        ],
        "image2": [
            "37",
            0
        ]
    },
    "class_type": "ImageBlend",
    "_meta": {
        "title": "Image Blend"
    }
},
```




## Prompts

### Main Prompt

```json
"22": {
    "inputs": {
        "text": "a cat",
        "clip": [
            "20",
            1
        ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
        "title": "PROMPT"
    }
},
```

```json
"33": {
    "inputs": {
        "text": "",
        "clip": [
            "20",
            1
        ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
        "title": "NEGATIVE PROMPT"
    }
},
```


### Prompt Splitting and Concatenation

**Mycraft** is designed to ensure that when writing a single large prompt, the neural network does not lose accuracy. To achieve this, "clips" are logically divided into parts, which proves to be more effective. For example, specific style triggers can be extracted from the prompt, and so on.

- [Impact Pack](https://github.com/ltdrdata/ComfyUI-Impact-Pack)

### Automatic Style Trigger for LoRA Styles

**Mycraft** includes a feature that eliminates the need to manually specify trigger words for activating LoRA (Low-Rank Adaptation) styles. It automatically assigns the appropriate value if the user provides a configuration `.json` file next to the LoRA `.safetensor` file.

Invisible to user in the **Mycraft** user interface.

```json
"23": {
    "inputs": {
        "text": "",
        "clip": [
            "20",
            1
        ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
        "title": "LORA PROMPT"
    }
},
```

### Constant Negative Prompt

Sometimes there are moments when the same words in a negative prompt, like "watermark" are enough to fix any generation issues.

Invisible to user in the **Mycraft** user interface.

```json
"34": {
    "inputs": {
        "text": "wrong hands, ugly figners, deformed body, watermark",
        "clip": [
            "20",
            1
        ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
        "title": "NEGATIVE PROMPT CONSTANT"
    }
},
```


## Power Lora Loader

This node allows applying multiple LoRA (Low-Rank Adaptation) styles simultaneously and blending them together.

- [rgthree-comfy](https://github.com/rgthree/rgthree-comfy.git)


```json
"20": {
    "inputs": {
        "PowerLoraLoaderHeaderWidget": {
            "type": "PowerLoraLoaderHeaderWidget"
        },
        "➕ Add Lora": "",
        "model": [
            "27",
            0
        ],
        "clip": [
            "27",
            1
        ]
    },
    "class_type": "Power Lora Loader (rgthree)",
    "_meta": {
        "title": "Power Lora Loader (rgthree)"
    }
},
```

## Mycraft UI Special Node with Generation Settings


This node is used to store information about generation in text form. 
It is necessary but still under development.


```json
"7777": {
    "inputs": {
        "text": ""
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
        "title": "Mycraft Settings"
    }
}
```

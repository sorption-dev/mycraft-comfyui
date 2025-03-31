... добавить картинок ...

# Get Started

## 1. Install

1. Install the [ComfyUi](https://github.com/comfyanonymous/ComfyUI).

2. Clone this repo into `custom_modules`:
    ```
    cd ComfyUI/custom_nodes
    git clone https://github.com/uauaouau/mycraft-ui.git
    ```

3. Start up ComfyUI.

## 2. Install ComfyUI Dependencies

This custom nodes are using to provide best user experience:

- [rgthree-comfy](https://github.com/rgthree/rgthree-comfy.git)
- [Impact Pack](https://github.com/ltdrdata/ComfyUI-Impact-Pack)
- [ComfyUI-load-image-from-url](https://github.com/tsogzark/ComfyUI-load-image-from-url)


Clone this repositories into `ComfyUI/custom_nodes` directory:

```
git clone https://github.com/rgthree/rgthree-comfy.git

git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git

git clone https://github.com/tsogzark/ComfyUI-load-image-from-url.git
```

Also you can install it via ComfyUI Manager.

# Workflows

This project are currently supports **text-to-text** and **image-to-image** workflows with **KSampler** sampler for models:

- SDXL (workflows/sdxl.json)

- Flux 1 Dev (workflows/flux.json)

### Custom Workflows

You can use your own workflow but there is some nodes that should exist with the constant node ids. [This is a list of nodes that **Mycraft** uses.](./CUSTOM_WORKFLOWS.md)



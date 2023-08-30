# NewYiri

本地运行的**小型**聊天机器人语言模型。

## 运行

```shell
NEW_YIRI_MODEL=wybxc/new-yiri NEW_YIRI_REVISION=b78622b6eed30e7ea591f9cb17dd326401bd553c python -m neoyiri
```

默认服务在 127.0.0.1:6001 上开启。

调用及响应格式兼容 https://github.com/Wybxc/TalkServer。

## 模型

模型在 [ernie3-nano-zh](https://huggingface.co/nghuyong/ernie-3.0-nano-zh) 基础上训练。可以在[此处](https://huggingface.co/wybxc/new-yiri)获取。

通过 `NEW_YIRI_MODEL` 与 `NEW_YIRI_REVISION` 环境变量控制加载的模型版本。

<br>

#### License

<sup>
Licensed under the <a href="LICENSE">Apache License, Version 2.0</a> (the "License");
you may not use this file except in compliance with the License.
</sup>

<sup>
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
</sup>
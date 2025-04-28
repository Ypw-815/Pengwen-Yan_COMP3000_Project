from django.shortcuts import render
from transformers import pipeline
from openai import OpenAI
from django.views.decorators.http import require_http_methods

from analyzer.models import AnalysisResult

# 配置DeepSeek API客户端
deepseek_client = OpenAI(
    api_key="sk-035ae85fd4ef4d8ea31919b725b416ca",
    base_url="https://api.deepseek.com"
)

# 预加载本地情感分析模型
local_model = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")


@require_http_methods(["GET", "POST"])
def analyze(request):
    result = None
    local_result = None
    deepseek_result = None
    text = ''

    if request.method == 'POST':
        # 获取文本内容
        text = request.POST.get('text', '')

        # 处理文件上传
        uploaded_file = request.FILES.get('file', None)
        if uploaded_file and uploaded_file.name.endswith('.txt'):
            try:
                # 读取文件内容
                file_content = uploaded_file.read().decode('utf-8')
                text = text + file_content  # 将文件内容作为分析文本
            except Exception as e:
                return render(request, 'analyzer/index.html', {
                    'error': f'文件读取失败: {str(e)}',
                    'text': text,
                    'local_result': local_result,
                    'deepseek_result': deepseek_result
                })

        if text:
            # 使用本地模型进行分析
            try:
                # 获取预测列表
                predictions = local_model(text)

                # 检查列表是否非空
                if isinstance(predictions, list) and len(predictions) > 0:
                    local_result = {
                        'model': 'DistilBERT',
                        'label': predictions[0]['label'],
                        'score': round(predictions[0]['score'], 4)
                    }
                else:
                    local_result = {'error': '未得到有效预测'}
            except Exception as e:
                local_result = {'error': f'本地模型错误: {str(e)}'}

            # 调用DeepSeek API进行分析
            try:
                response = deepseek_client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {
                            "role": "system",
                            "content": "You must strictly output only one of the following words: 'Positive', 'Negative', or 'Neutral'. Do not provide any explanations, additional text, or variations. Only one of these three words is allowed as the output."
                        },
                        {
                            "role": "user",
                            "content": f"Based on the following text, output only 'Positive', 'Negative', or 'Neutral': {text}"
                        }
                    ],
                    temperature=0,
                    max_tokens=1
                )
                if response.choices and len(response.choices) > 0:
                    valid_labels = {"POSITIVE", "NEGATIVE", "NEUTRAL"}
                    api_label = response.choices[0].message.content.strip().upper()
                    # 如果 API 返回的标签不在有效范围内，设置为默认值（如 "Neutral"）
                    if api_label not in valid_labels:
                        api_label = "NEUTRAL"
                    deepseek_result = {
                        'model': 'DeepSeek',
                        'label': api_label
                    }
                else:
                    deepseek_result = {'error': '未收到有效API响应'}
            except Exception as e:
                deepseek_result = {'error': f'API错误: {str(e)}'}

            # 保存分析结果到数据库
            if deepseek_result and 'error' not in deepseek_result:
                AnalysisResult.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    text=text,
                    local_label=local_result.get('label') if local_result else None,
                    local_score=local_result.get('score') if local_result else None,
                    deepseek_label=deepseek_result['label']
                )

    return render(request, 'analyzer/index.html', {
        'text': text,
        'local_result': local_result,
        'deepseek_result': deepseek_result
    })

# @require_http_methods(["GET", "POST"])
# def analyze(request):
#     result = None
#     local_result = None
#     deepseek_result = None
#     text = ''
#
#     if request.method == 'POST':
#         # 添加限速逻辑（10秒内只能提交一次）
#         # ip = request.META.get('REMOTE_ADDR', '')
#         # cache_key = f"ratelimit:{ip}"
#         # if cache.get(cache_key):
#         #     return render(request, 'error.html', {'error': '操作过于频繁，请10秒后再试'})
#         # cache.set(cache_key, True, timeout=1)
#
#         text = request.POST.get('text', '')
#         if text:
#             # accounts/views.py 修改部分
#             try:
#                 # 获取预测列表
#                 predictions = local_model(text)
#
#                 # 检查列表是否非空
#                 if isinstance(predictions, list) and len(predictions) > 0:
#                     local_result = {
#                         'model': 'DistilBERT',
#                         'label': predictions[0]['label'],
#                         'score': round(predictions[0]['score'], 4)
#                     }
#                 else:
#                     local_result = {'error': '未得到有效预测'}
#             except Exception as e:
#                 local_result = {'error': f'本地模型错误: {str(e)}'}
#
#
#             # 调用DeepSeek API
#             try:
#                 response = deepseek_client.chat.completions.create(
#                     model="deepseek-chat",
#                     messages=[
#                         {
#                             "role": "system",
#                             "content": "You must strictly output only one of the following words: 'Positive', 'Negative', or 'Neutral'. Do not provide any explanations, additional text, or variations. Only one of these three words is allowed as the output."
#                         },
#                         {
#                             "role": "user",
#                             "content": f"Based on the following text, output only 'Positive', 'Negative', or 'Neutral': {text}"
#                         }
#                     ],
#                     temperature=0,
#                     max_tokens=1
#                 )
#                 if response.choices and len(response.choices) > 0:
#                     valid_labels = {"POSITIVE", "NEGATIVE", "NEUTRAL"}
#                     api_label = response.choices[0].message.content.strip().upper()
#                     # 如果 API 返回的标签不在有效范围内，设置为默认值（如 "Neutral"）
#                     if api_label not in valid_labels:
#                         api_label = "NEUTRAL"
#                     deepseek_result = {
#                         'model': 'DeepSeek',
#                         'label': api_label
#                     }
#                 else:
#                     deepseek_result = {'error': '未收到有效API响应'}
#             except Exception as e:
#                 deepseek_result = {'error': f'API错误: {str(e)}'}
#
#             # 保存分析结果到数据库
#             if deepseek_result and 'error' not in deepseek_result:
#                 AnalysisResult.objects.create(
#                     user=request.user if request.user.is_authenticated else None,
#                     text=text,
#                     local_label=deepseek_result['label'],
#                     local_score=deepseek_result.get('score'),
#                     deepseek_label=deepseek_result['label']
#                 )
#
#     print("------------------------")
#     print(local_result, deepseek_result)
#     print("------------------------")
#
#     return render(request, 'analyzer/index.html', {
#         'text': text,
#         'local_result': local_result,
#         'deepseek_result': deepseek_result
#     })



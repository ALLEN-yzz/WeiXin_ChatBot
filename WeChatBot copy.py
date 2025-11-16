from openai import OpenAI
from wxauto import WeChat
import time
import json
import re

class WeChatBot:
    def __init__(self):
        self.client = OpenAI(api_key="sk-80f0ad767cd84fd6ad3dc2ba3e89820a",base_url="https://api.deepseek.com")
        self.wx = WeChat()
        # 可以监听特定联系人或群组，或使用空列表监听所有
        self.listen_list = [
            "深渊"
        ]  # 空列表表示监听所有联系人
        for whoItem in self.listen_list:
            self.wx.AddListenChat(who=whoItem)
        
        # 加载采样知识库
        self.knowledge_base = self.load_knowledge_base()
        print("采样知识库功能已启用，可以回答基于知识的问题")
    
    # 定义知识库文件路径（请用户替换为自己的知识库文件）
    KNOWLEDGE_BASE_FILE = "sampling_knowledge_base_example.json"
    
    def load_knowledge_base(self):
        """加载采样知识库文件"""
        try:
            with open(self.KNOWLEDGE_BASE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"加载采样知识库失败: {e}")
            print("注意：当前使用的是示例知识库，请根据README中的说明配置您自己的知识库。")
            return {"knowledge_items": []}
    
    def search_knowledge_base(self, query):
        """基于关键词在采样知识库中检索相关答案"""
        query = query.lower()
        best_match = None
        max_score = 0
        
        for item in self.knowledge_base.get("knowledge_items", []):
            question = item["question"].lower()
            # 计算匹配得分（基于共同关键词数量）
            # 修改正则表达式以更好地处理中文文本
            query_words = set(re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z0-9]+', query))
            question_words = set(re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z0-9]+', question))
            common_words = query_words.intersection(question_words)
            score = len(common_words)
            
            # 精确匹配优先
            if query == question:
                return item["answer"]
            
            # 特别处理地区名称的匹配
            provinces = ['广东省', '上海市', '重庆市', '江苏省', '安徽省', '四川省', '江西省', '贵州省', '吉林省', '河北省', '河南省', '福建省', '云南省', '湖北省', '浙江省', '湖南省', '宁夏回族自治区', '山东省', '辽宁省', '海南省', '广西壮族自治区', '山西省', '陕西省', '甘肃省', '天津市']
            cities = ['汕头市', '金平区', '静安区', '长宁区', '渝中区', '宿迁市', '湖滨新区', '合肥市', '蜀山区', '自贡市', '赣州市', '章贡区', '抚州市', '黔南布', '长春市', '南关区', '邯郸市', '邯山区', '邢台市', '南和区', '郑州市', '福州市', '鼓楼区', '福清市', '莆田市', '涵江区', '三明市', '南平市', '延平区', '昆明市', '呈贡区', '曲靖市', '德宏市', '浦东新区', '闵行区', '武汉市', '硚口区', '深圳市', '罗湖区', '苏州市', '相城区', '厦门市', '海沧区', '佛山市', '禅城区', '茂名市', '化州市', '西山区', '新郑市', '开封市', '南阳市', '广州市', '番禺区', '长沙市', '石家庄市', '银川市', '南京市', '杭州市', '萧山区', '温州市', '乐清市', '包河区', '静安区', '槐荫区', '沈阳市', '营口市', '海口市', '南充市', '钦州市', '九龙坡区', '鹰潭市', '中山市', '金华市', '永康市', '广安市', '龙岗区', '德州市', '德城区', '平阳县', '滨海新区', '西固区', '新都区', '桂林市', '龙岩市', '小店区', '咸阳市', '秦都区', '市南区', '贵阳市', '花溪区', '唐山市', '路南区', '崇川区', '拱墅区', '海州区', '南湖区']
            
            # 如果问题中包含地区名称，增加匹配权重
            for province in provinces:
                if province in query and province in question:
                    score += 2
            for city in cities:
                if city in query and city in question:
                    score += 1
            
            if score > max_score:
                max_score = score
                best_match = item["answer"]
        
        # 只有当找到足够相关的匹配时才返回知识库答案
        return best_match if max_score > 1 else None

    def __ask(self,msg):
        # 首先尝试从知识库中获取答案
        kb_answer = self.search_knowledge_base(msg)
        if kb_answer:
            return kb_answer
        
        # 如果知识库中没有相关答案，则调用大模型
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你叫姚姚乐，是一个专业的销售。冷酷高冷，身高180cm。说话风趣幽默，每次回答不超过20个字"},
                {"role": "user", "content": msg}
            ],
            stream = False
        )
        return response.choices[0].message.content

    def run(self):
        wait = 2
        print("微信监控已启动，正在监听以下聊天:", self.listen_list)
        while True:           
            msgs = self.wx.GetListenMessage()
            for chat in msgs:
                    msg = msgs.get(chat)
                    for item in msg:
                        if item.type == "friend" :
                            reply = self.__ask(item.content)
                            print(f"接受【{item.sender}】的消息：{item.content}")
                            print(f"回复【{item.sender}】的消息：{reply}")
                            # 使用WeChat实例发送消息到指定聊天
                            self.wx.SendMsg(reply, item.sender)
            time.sleep(wait)
if __name__ == "__main__":
    bot = WeChatBot()
    bot.run()
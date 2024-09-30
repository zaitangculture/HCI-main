import gensim
import gensim.corpora as corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
import nltk

# 下载停用词
nltk.download('stopwords')

# 示例文档
texts = [
    "I love reading books about machine learning.",
    "Machine learning is a fascinating field.",
    "Books about data science are very interesting.",
    "I enjoy learning about new technologies.",
    "Data science and machine learning are closely related."
]

# 预处理文本
stop_words = stopwords.words('english')
texts = [[word for word in document.lower().split() if word not in stop_words] for document in texts]

# 创建词典
id2word = corpora.Dictionary(texts)

# 创建语料库
corpus = [id2word.doc2bow(text) for text in texts]

# 训练LDA模型
lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=2, random_state=42, update_every=1, passes=10, alpha='auto', per_word_topics=True)

# 打印主题
for idx, topic in lda_model.print_topics(-1):
    print(f"Topic: {idx} \nWords: {topic}\n")

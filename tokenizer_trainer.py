import tokenizers as tok
import transformers as tr


# TODO Токенизатор
tknzr = tok.Tokenizer(tok.models.BPE(unk_token="[UNK]"))  # * Определяем модель токенизации(BPE) и определяем замену для неизвестных токенов([UNK])
tknzr.pre_tokenizer = tok.pre_tokenizers.Sequence([tok.pre_tokenizers.Whitespace(), tok.pre_tokenizers.Punctuation()])  # * Задаем характер ПРЕтокенизации. В нашем случае Whitespace - разбиение по пробелам с сохранением координат(индексов)


# TODO Тренировка токенизатора
trainer = tok.trainers.BpeTrainer(special_tokens=["[PAD]"])  # * Создаем тренера для BPE-токенизатора и добавляем специальный токен [PAD]
tknzr.train(["dataset.txt"], trainer) # * Тренируем токенизатор на собранном датасете
tknzr.enable_padding() # * Включаем механизм паддинга


vocab = tknzr.get_vocab() # * Получаем словарь из обученного токенизатора
hug_tokenizer = tr.PreTrainedTokenizerFast(tokenizer_object = tknzr) # * Переводим токенизатор в понятный трансформерам формат


config = tr.GPT2Config(
    vocab_size=len(vocab),
    bos_token_id=hug_tokenizer.token_to_id("[CLS]"),
    eos_token_id=hug_tokenizer.token_to_id("[EOS]"),
)
gpt = tr.GPT2LMHeadModel(config)
from spacy.en import English
from pyspark import keyword_only
from pyspark.ml.util import Identifiable
from pyspark.sql.functions import udf
from spark.ml.pipeline import Transformer
from spark.ml.param.shared import HasInputCol, HasOutputCol
from pyspark.sql.types import ArrayType, StringType


class ParsingTransformer(Transformer, HasInputCol, HasOutputCol):

    @keyword_only
    def __init__(self, inputCol=None, oututCol=None):
        super(ParsingTransformer, self).__init__()
        kwargs = self.__init__._input_kwargs
        self.setParams(**kwargs)

    @keyword_only
    def setParams(self, inputCol=None, outputCol=None):
        kwargs = self.setParams._input_kwargs
        return self._set(**kwargs)

    def _transform(self, dataset):
        parser = English()

        # def f(s):
        #     tokens = parser(s)
        #     return [tok.lower_ for tok in tokens]
        #
        # t = ArrayType(StringType())
        # out_col = self.getOutputCol()
        # in_col = self.dataset[self.getInputCol()]
        # return dataset.withColumn(out_col, udf(f, t)(in_col))

        parser = udf(lambda excerpt: [t.lower_ for t in parser(excerpt)],
                     ArrayType(StringType()))
        inCol = self.getInputCol()
        outCol = self.getOutputCol()
        return dataset.withColumn(outCol, parser(inCol))

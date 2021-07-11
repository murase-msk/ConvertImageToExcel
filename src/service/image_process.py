from dataclasses import dataclass
from typing import Dict, List
from google.cloud import vision
from shapely.geometry.polygon import Polygon


@dataclass(frozen=True)
class Block:
    text: str
    id: int
    confidence: float
    poly: Polygon


@dataclass(frozen=True)
class Word:
    text: str
    blockId: int
    confidence: float
    poly: Polygon


@dataclass(frozen=True)
class SearchArea:
    poly: Polygon


class ImageProcess:
    """ google vision apiを使った画像処理関係
    """

    def __init__(self):
        return

    def getLabels(self, binaryFile: bytes) -> list[str]:
        """ 保存された画像のファイルパス(filePath)からラベルを取得
        """
        ##################################################
        # Google Vision API
        client = vision.ImageAnnotatorClient()
        # file_name = os.path.abspath(filePath)
        # with io.open(file_name, 'rb') as image_file:
        #     content = image_file.read()
        image = vision.Image(content=binaryFile)
        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        labelList: list[str] = []
        for label in labels:
            labelList.append(label.description)

        return labelList

    def detectText(self, binaryFile: bytes) -> list[str]:
        """ファイルパスからテキスト情報を取得する
        """

        client = vision.ImageAnnotatorClient()
        # with io.open(filePath, 'rb') as image_file:
        #     content = image_file.read()
        image = vision.Image(content=binaryFile)
        response = client.text_detection(image=image)
        texts = response.text_annotations

        outputList: list = []

        for text in texts:
            oneText: dict = {}
            oneText["text"] = text.description
            oneText["p0"] = {"x": text.bounding_poly.vertices[0].x, "y": text.bounding_poly.vertices[0].y}
            oneText["p1"] = {"x": text.bounding_poly.vertices[1].x, "y": text.bounding_poly.vertices[1].y}
            oneText["p2"] = {"x": text.bounding_poly.vertices[2].x, "y": text.bounding_poly.vertices[2].y}
            oneText["p3"] = {"x": text.bounding_poly.vertices[3].x, "y": text.bounding_poly.vertices[3].y}
            outputList.append(oneText)
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        return outputList

    def detectDocumentText(self, binaryFile: bytes) -> list[any]:
        """ ドキュメントテキストの検出
        """

        client = vision.ImageAnnotatorClient()
        # with io.open(filePath, 'rb') as image_file:
        #     content = image_file.read()
        # image = vision.Image(content=content)
        # response = client.text_detection(image=image)
        response = client.annotate_image({
            'image': vision.Image(content=binaryFile),
            'image_context': {"language_hints": ["en", "ja"]},
            'features': [{'type_': vision.Feature.Type.DOCUMENT_TEXT_DETECTION}],
        })
        # CROP_HINTS = 9
        # DOCUMENT_TEXT_DETECTION = 11
        # FACE_DETECTION = 1
        # IMAGE_PROPERTIES = 7
        # LABEL_DETECTION = 4
        # LANDMARK_DETECTION = 2
        # LOGO_DETECTION = 3
        # OBJECT_LOCALIZATION = 19
        # PRODUCT_SEARCH = 12
        # SAFE_SEARCH_DETECTION = 6
        # TEXT_DETECTION = 5
        # TYPE_UNSPECIFIED = 0
        # WEB_DETECTION = 10
        document = response.full_text_annotation
        outputlList: List = []
        for page in document.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        # for symbol in word.symbols:
                        # print(symbol.text)
                        outputlList.append([(word.bounding_box.vertices[0].x, word.bounding_box.vertices[0].y),
                                            # (word.bounding_box.vertices[1].x, word.bounding_box.vertices[1].y),
                                            (word.bounding_box.vertices[2].x, word.bounding_box.vertices[2].y)  # ,
                                            # (word.bounding_box.vertices[3].x, word.bounding_box.vertices[3].y)
                                            ])
                    outputlList.append([(paragraph.bounding_box.vertices[0].x, paragraph.bounding_box.vertices[0].y),
                                        # (paragraph.bounding_box.vertices[1].x, paragraph.bounding_box.vertices[1].y),
                                        (paragraph.bounding_box.vertices[2].x, paragraph.bounding_box.vertices[2].y)  # ,
                                        # (paragraph.bounding_box.vertices[3].x, paragraph.bounding_box.vertices[3].y)
                                        ])
        return outputlList

    def detectDocumentTextV2ForImage(self, binaryFile: bytes) -> Dict[List[Word], List[Block]]:
        """ ドキュメントテキストの検出(image)
        """
        client = vision.ImageAnnotatorClient()
        # with io.open(filePath, 'rb') as image_file:
        #     content = image_file.read()

        response = client.annotate_image({
            'image': vision.Image(content=binaryFile),
            'image_context': {"language_hints": ["en", "ja"]},
            'features': [{'type_': vision.Feature.Type.DOCUMENT_TEXT_DETECTION}]
        })
        # outputList.append({"blocks": outputBlockList, "words": outputWordlList})
        return self.__getDocumentData(response.full_text_annotation)

    def detectDocumentTextForPdf(self, binaryFile: bytes) -> Dict[List[Word], List[Block]]:
        """ ドキュメントテキストの検出(PDF)
        """
        client = vision.ImageAnnotatorClient()
        # with io.open(filePath, 'rb') as image_file:
        #     binary_content = image_file.read()
        req = vision.AnnotateFileRequest(
            # バイナリファイルの指定
            input_config=vision.InputConfig(content=binaryFile, mime_type='application/pdf'),
            # 検出したい特徴の指定
            features=[vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)],
            # 言語ヒント
            image_context=vision.ImageContext(language_hints=["en", "ja"]),
            # 検出対象ページの指定
            pages=[1, 2]  # 同期の場合、5ページ以上指定不可
        )
        # batch_annotate_files呼び出し。リクエストがリストであることに注意。
        batch_response = client.batch_annotate_files(requests=[req])
        document = batch_response.responses[0].responses[0].full_text_annotation
        return self.__getPdfDocumentData(document)

    def __getDocumentData(self, full_text_annotation) -> Dict[List[Word], List[Block]]:
        """
        full_text_annotationを解析してPythonで扱えるデータで返す(image)
        @ param full_text_annotation
        """
        outputWordlList: List[Word] = []
        outputBlockList: List[Block] = []
        for page in full_text_annotation.pages:
            blockId: int = 0
            for block in page.blocks:
                oneBlock: str = ""
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        oneWord: str = ""
                        for symbol in word.symbols:
                            oneWord = oneWord + symbol.text
                            oneBlock = oneBlock + symbol.text
                        outputWordlList.append(
                            Word(
                                text=oneWord,
                                blockId=blockId,
                                confidence=word.confidence,
                                poly=Polygon(
                                    [
                                        (word.bounding_box.vertices[0].x, word.bounding_box.vertices[0].y),
                                        (word.bounding_box.vertices[1].x, word.bounding_box.vertices[1].y),
                                        (word.bounding_box.vertices[2].x, word.bounding_box.vertices[2].y),
                                        (word.bounding_box.vertices[3].x, word.bounding_box.vertices[3].y)
                                    ]
                                )
                            )
                        )
                blockId = blockId + 1
                outputBlockList.append(
                    Block(
                        text=oneBlock,
                        id=blockId,
                        confidence=block.confidence,
                        poly=Polygon(
                            [
                                (block.bounding_box.vertices[0].x, block.bounding_box.vertices[0].y),
                                (block.bounding_box.vertices[1].x, block.bounding_box.vertices[1].y),
                                (block.bounding_box.vertices[2].x, block.bounding_box.vertices[2].y),
                                (block.bounding_box.vertices[3].x, block.bounding_box.vertices[3].y)
                            ]
                        )
                    )
                )
        return {"blocks": outputBlockList, "words": outputWordlList}

    def __getPdfDocumentData(self, full_text_annotation) -> Dict[List[Word], List[Block]]:
        """
        full_text_annotationを解析してPythonで扱えるデータで返す(PDF)
        @ param full_text_annotation
        """
        outputWordlList: List[Word] = []
        outputBlockList: List[Block] = []
        for page in full_text_annotation.pages:
            blockId: int = 0
            for block in page.blocks:
                oneBlock: str = ""
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        oneWord: str = ""
                        for symbol in word.symbols:
                            oneWord = oneWord + symbol.text
                            oneBlock = oneBlock + symbol.text
                        outputWordlList.append(
                            Word(
                                text=oneWord,
                                blockId=blockId,
                                confidence=word.confidence,
                                poly=Polygon(
                                    [
                                        (word.bounding_box.normalized_vertices[0].x, word.bounding_box.normalized_vertices[0].y),
                                        (word.bounding_box.normalized_vertices[1].x, word.bounding_box.normalized_vertices[1].y),
                                        (word.bounding_box.normalized_vertices[2].x, word.bounding_box.normalized_vertices[2].y),
                                        (word.bounding_box.normalized_vertices[3].x, word.bounding_box.normalized_vertices[3].y)
                                    ]
                                )
                            )
                        )
                blockId = blockId + 1
                outputBlockList.append(
                    Block(
                        text=oneBlock,
                        id=blockId,
                        confidence=block.confidence,
                        poly=Polygon(
                            [
                                (block.bounding_box.normalized_vertices[0].x, block.bounding_box.normalized_vertices[0].y),
                                (block.bounding_box.normalized_vertices[1].x, block.bounding_box.normalized_vertices[1].y),
                                (block.bounding_box.normalized_vertices[2].x, block.bounding_box.normalized_vertices[2].y),
                                (block.bounding_box.normalized_vertices[3].x, block.bounding_box.normalized_vertices[3].y)
                            ]
                        )
                    )
                )
        return {"blocks": outputBlockList, "words": outputWordlList}

    def pickUpTextFromSearchAreas(self, binaryFile: bytes, searchAreas: List[SearchArea]) -> List[str]:
        """ 指定範囲からテキストを抜き出す
        """
        client = vision.ImageAnnotatorClient()
        req = vision.AnnotateFileRequest(
            # バイナリファイルの指定
            input_config=vision.InputConfig(content=binaryFile, mime_type='application/pdf'),
            # 検出したい特徴の指定
            features=[vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)],
            # 言語ヒント
            image_context=vision.ImageContext(language_hints=["en", "ja"]),
            # 検出対象ページの指定
            pages=[1]  # 同期の場合、5ページ以上指定不可
        )
        # batch_annotate_files呼び出し。リクエストがリストであることに注意。
        batch_response = client.batch_annotate_files(requests=[req])
        document = batch_response.responses[0].responses[0].full_text_annotation
        return self.__getPdfDocumentDataFromSearchAreas(document, searchAreas)

    def __getPdfDocumentDataFromSearchAreas(self, full_text_annotation, searchAreas: List[SearchArea]) -> List[str]:
        """ full_text_annotationを解析して指定範囲からテキストを抜き出す
        """
        outputTextList: List[str] = []
        i: int = 0
        for i in range(len(searchAreas)):
            outputTextList.append("")

        for page in full_text_annotation.pages:
            blockId: int = 0
            for block in page.blocks:
                oneBlockText: str = ""
                for paragraph in block.paragraphs:
                    oneParagraphText: str = ""
                    for word in paragraph.words:
                        oneWordText: str = ""
                        for symbol in word.symbols:
                            oneWordText = oneWordText + symbol.text
                            oneParagraphText = oneParagraphText + symbol.text
                            oneBlockText = oneBlockText + symbol.text

                        oneWord: Word = Word(
                            text=oneWordText,
                            blockId=blockId,
                            confidence=word.confidence,
                            poly=Polygon(
                                [
                                    (word.bounding_box.normalized_vertices[0].x, word.bounding_box.normalized_vertices[0].y),
                                    (word.bounding_box.normalized_vertices[1].x, word.bounding_box.normalized_vertices[1].y),
                                    (word.bounding_box.normalized_vertices[2].x, word.bounding_box.normalized_vertices[2].y),
                                    (word.bounding_box.normalized_vertices[3].x, word.bounding_box.normalized_vertices[3].y)
                                ]
                            )
                        )
                        # このワードが取り出したい文字範囲の中に含まれれば抜き出す
                        i: int = 0
                        for i in range(len(searchAreas)):
                            if searchAreas[i].poly.contains(oneWord.poly.centroid):
                                outputTextList[i] = outputTextList[i] + oneWord.text
                blockId = blockId + 1
        return outputTextList

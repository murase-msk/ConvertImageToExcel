import os
import io
from google.cloud import vision


class ImageProcess:
    """ google vision apiを使った画像処理関係
    """

    # def __init__(self):

    def getLabels(filePath: str) -> list[str]:
        """ 保存された画像のファイルパス(filePath)からラベルを取得
        """
        #
        # Google Vision API
        #
        # Instantiates a client
        client = vision.ImageAnnotatorClient()
        # The name of the image file to annotate
        file_name = os.path.abspath(filePath)
        # Loads the image into memory
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        labelList: list[str] = []
        for label in labels:
            labelList.append(label.description)

        return labelList

    def detectText(filePath: str) -> list[str]:
        """ファイルパスからテキスト情報を取得する
        """

        client = vision.ImageAnnotatorClient()
        with io.open(filePath, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        print('Texts:')

        for text in texts:
            print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        return []

    def detectDocumentText(filePath: str) -> list[any]:
        """ ドキュメントテキストの検出
        """

        client = vision.ImageAnnotatorClient()
        with io.open(filePath, 'rb') as image_file:
            content = image_file.read()
        # image = vision.Image(content=content)
        # response = client.text_detection(image=image)
        response = client.annotate_image({
            'image': vision.Image(content=content),
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
        outputlList: list = []
        for page in document.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        # for symbol in word.symbols:
                        # print(symbol.text)
                        # print(str(symbol.bounding_box.vertices[0].x) + " " + str(symbol.bounding_box.vertices[0].y))
                        # print(str(symbol.bounding_box.vertices[1].x) + " " + str(symbol.bounding_box.vertices[1].y))
                        # print(str(symbol.bounding_box.vertices[2].x) + " " + str(symbol.bounding_box.vertices[2].y))
                        # print(str(symbol.bounding_box.vertices[3].x) + " " + str(symbol.bounding_box.vertices[3].y))
                        # print(word.confidence)
                        # print(str(word.bounding_box.vertices[0].x) + " " + str(word.bounding_box.vertices[0].y))
                        # print(str(word.bounding_box.vertices[1].x) + " " + str(word.bounding_box.vertices[1].y))
                        # print(str(word.bounding_box.vertices[2].x) + " " + str(word.bounding_box.vertices[2].y))
                        # print(str(word.bounding_box.vertices[3].x) + " " + str(word.bounding_box.vertices[3].y))
                        outputlList.append([(word.bounding_box.vertices[0].x, word.bounding_box.vertices[0].y),
                                            # (word.bounding_box.vertices[1].x, word.bounding_box.vertices[1].y),
                                            (word.bounding_box.vertices[2].x, word.bounding_box.vertices[2].y)  # ,
                                            # (word.bounding_box.vertices[3].x, word.bounding_box.vertices[3].y)
                                            ])
                    # print(paragraph.confidence)
                    # print(str(paragraph.bounding_box.vertices[0].x) + " " + str(paragraph.bounding_box.vertices[0].y))
                    # print(str(paragraph.bounding_box.vertices[1].x) + " " + str(paragraph.bounding_box.vertices[1].y))
                    # print(str(paragraph.bounding_box.vertices[2].x) + " " + str(paragraph.bounding_box.vertices[2].y))
                    # print(str(paragraph.bounding_box.vertices[3].x) + " " + str(paragraph.bounding_box.vertices[3].y))
                    outputlList.append([(paragraph.bounding_box.vertices[0].x, paragraph.bounding_box.vertices[0].y),
                                        # (paragraph.bounding_box.vertices[1].x, paragraph.bounding_box.vertices[1].y),
                                        (paragraph.bounding_box.vertices[2].x, paragraph.bounding_box.vertices[2].y)  # ,
                                        # (paragraph.bounding_box.vertices[3].x, paragraph.bounding_box.vertices[3].y)
                                        ])
                # print(block.block_type)
                # print(block.confidence)
                # print(str(block.bounding_box.vertices[0].x) + " " + str(block.bounding_box.vertices[0].y))
                # print(str(block.bounding_box.vertices[1].x) + " " + str(block.bounding_box.vertices[1].y))
                # print(str(block.bounding_box.vertices[2].x) + " " + str(block.bounding_box.vertices[2].y))
                # print(str(block.bounding_box.vertices[3].x) + " " + str(block.bounding_box.vertices[3].y))
                # outputlList.append([(block.bounding_box.vertices[0].x, block.bounding_box.vertices[0].y),
                #                     # (block.bounding_box.vertices[1].x, block.bounding_box.vertices[1].y),
                #                     (block.bounding_box.vertices[2].x, block.bounding_box.vertices[2].y)  # ,
                #                     # (block.bounding_box.vertices[3].x, block.bounding_box.vertices[3].y)
                #                     ])
            # print(page.page_type)
            # print(page.confidence)
            # print(str(page.bounding_box.vertices[0].x) + " " + str(page.bounding_box.vertices[0].y))
            # print(str(page.bounding_box.vertices[1].x) + " " + str(page.bounding_box.vertices[1].y))
            # print(str(page.bounding_box.vertices[2].x) + " " + str(page.bounding_box.vertices[2].y))
            # print(str(page.bounding_box.vertices[3].x) + " " + str(page.bounding_box.vertices[3].y))
            # outputlList.append([(page.bounding_box.vertices[0].x, page.bounding_box.vertices[0].y),
                # (page.bounding_box.vertices[1].x, page.bounding_box.vertices[1].y),
                # (page.bounding_box.vertices[2].x, page.bounding_box.vertices[2].y)  # ,
                # (page.bounding_box.vertices[3].x, page.bounding_box.vertices[3].y)
                # ])
        return outputlList

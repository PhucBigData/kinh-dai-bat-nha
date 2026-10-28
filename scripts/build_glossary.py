#!/usr/bin/env python3
"""
Prajñā Buddhist Glossary Dataset Builder
Creates reader/data/glossary.json containing curated, authentic doctrinal terms.
"""

import json
import os

GLOSSARY_TERMS = [
    {
        "id": "bat-nha-ba-la-mat-da",
        "term": "Bát-nhã Ba-la-mật-đa",
        "sanskrit": "Prajñāpāramitā",
        "chinese": "般若波羅蜜多",
        "category": "Triết học Bát Nhã",
        "brief": "Trí tuệ viên mãn rốt ráo, đưa hành giả vượt qua biển khổ sanh tử cập bến bờ giác ngộ giải thoát.",
        "detail": "Bát-nhã là trí tuệ thấu suốt thực tướng tánh Không của muôn pháp, không bị vướng mắc vào bất kỳ tướng hư vọng nào. Ba-la-mật-đa nghĩa là 'đáo bỉ ngạn' (đến bờ kia), chỉ sự cứu cánh viên mãn của trí tuệ Phật thừa, là mẹ sinh ra chư Phật trong ba đời."
    },
    {
        "id": "tanh-khong",
        "term": "Tánh Không",
        "sanskrit": "Śūnyatā",
        "chinese": "空性",
        "category": "Triết học Bát Nhã",
        "brief": "Bản chất phi tự tánh, không độc lập, do duyên sinh của mọi hiện tượng trong vũ trụ.",
        "detail": "Tánh Không không phải là hư vô hay không có gì (ngoan không), mà là bản chất chân thật của vạn pháp: vì do các duyên hòa hợp mà thành nên không có tự thể bất biến, thường hằng. Nhờ tánh Không mà vạn pháp biến dịch, người tu có thể đoạn trừ phiền não và đạt giải thoát."
    },
    {
        "id": "vo-so-dac",
        "term": "Vô sở đắc",
        "sanskrit": "Anupalambha",
        "chinese": "無所得",
        "category": "Triết học Bát Nhã",
        "brief": "Cốt tủy của giáo lý Bát Nhã: tâm hoàn toàn vắng bặt ý niệm sở đắc, sở thủ, không chấp trụ vào bất kỳ quả vị hay pháp nào.",
        "detail": "Trong Kinh Đại Bát Nhã, Đức Phật thường dạy 'Dĩ vô sở đắc vi phương tiện'. Nếu còn thấy có pháp để chứng, có Bồ-đề để đắc thì vẫn còn ngã và pháp. Khi đạt đến cảnh giới vô sở đắc, tâm thanh tịnh tự tại như hư không, đó mới là chân thật đắc Bát-nhã Ba-la-mật-đa."
    },
    {
        "id": "chan-nhu",
        "term": "Chân Như",
        "sanskrit": "Tathatā",
        "chinese": "真如",
        "category": "Triết học Bát Nhã",
        "brief": "Bản thể như chân, như thật của muôn pháp; chân thật không hư dối, hằng thường bất biến.",
        "detail": "'Chân' là không biến đổi theo thời gian; 'Như' là bình đẳng khắp mười phương không sai biệt. Chân Như là thật tánh của pháp giới, xa lìa mọi vọng tưởng phân biệt nhị nguyên, là tự tánh thanh tịnh bản nhiên của tâm."
    },
    {
        "id": "thuc-tuong",
        "term": "Thực tướng",
        "sanskrit": "Dharmatā",
        "chinese": "實相",
        "category": "Triết học Bát Nhã",
        "brief": "Tướng chân thật của muôn pháp, vốn là 'vô tướng', vượt thoát khỏi mọi tướng trạng sinh diệt hư dối.",
        "detail": "Kinh dạy: 'Thực tướng của các pháp chính là phi tướng'. Mọi tướng trạng mắt thấy tai nghe đều do duyên khởi sinh diệt tạm bợ. Nhận ra được thực tướng tức là thấy được tánh Không vô sai biệt của các pháp."
    },
    {
        "id": "huyen-hoa",
        "term": "Huyễn hóa",
        "sanskrit": "Māyā",
        "chinese": "幻化",
        "category": "Triết học Bát Nhã",
        "brief": "Thí dụ then chốt của Bát Nhã: vạn pháp ví như nhà ảo thuật biến hóa, có hiện tướng nhưng không có tự thể thật.",
        "detail": "Tất cả sắc, thọ, tưởng, hành, thức cho đến quả vị Niết-bàn đều như mộng, như huyễn, như bọt nước, như bóng hình. Thấu đạt được lý huyễn hóa thì Bồ-tát tuy hóa độ vô lượng chúng sanh mà không thấy có chúng sanh nào được diệt độ."
    },
    {
        "id": "bo-de-tam",
        "term": "Bồ-đề-tâm",
        "sanskrit": "Bodhicitta",
        "chinese": "菩提心",
        "category": "Bồ Tát Đạo",
        "brief": "Tâm nguyện giác ngộ tối thượng: trên cầu Phật đạo, dưới hóa độ tất cả chúng sanh không mệt mỏi.",
        "detail": "Bồ-đề-tâm là cội nguồn của mọi hạnh nguyện Bồ-tát, gồm Tục đế Bồ-đề-tâm (lòng đại bi cứu khổ) và Chân đế Bồ-đề-tâm (trí tuệ thấu suốt tánh Không). Không phát Bồ-đề-tâm thì không thể thực hành Bát-nhã Ba-la-mật-đa."
    },
    {
        "id": "tat-ba-nha",
        "term": "Tát-bà-nhã",
        "sanskrit": "Sarvajña",
        "chinese": "薩婆若",
        "category": "Trí Tuệ & Quả Vị",
        "brief": "Nhất thiết trí (Trí tuệ toàn tri), trí thấy suốt toàn thể vũ trụ vạn pháp của bậc Toàn Giác.",
        "detail": "Tát-bà-nhã là trí đức của Đức Phật, thấu rõ tất cả pháp tướng và pháp tánh của vạn vật trong ba đời mà không hề chướng ngại. Bát-nhã Ba-la-mật-đa chính là cỗ xe đưa hành giả tiến nhập biển lớn Tát-bà-nhã."
    },
    {
        "id": "nhat-thiet-chung-tri",
        "term": "Nhất thiết chủng trí",
        "sanskrit": "Sarvākārajñatā",
        "chinese": "一切種智",
        "category": "Trí Tuệ & Quả Vị",
        "brief": "Trí tuệ cao nhất trong ba trí: thấu đạt cùng tột cả tổng tướng (tánh Không) lẫn biệt tướng (duyên khởi) của vạn pháp.",
        "detail": "Gồm ba bậc: Nhất thiết trí (thấu triệt tánh Không của hàng Thanh văn), Đạo chủng trí (thấu hiểu các phương tiện hóa độ của Bồ-tát), và Nhất thiết chủng trí (trí giác ngộ toàn diện, cứu cánh của chư Phật)."
    },
    {
        "id": "vo-sanh-phap-nhan",
        "term": "Vô sanh pháp nhẫn",
        "sanskrit": "Anutpattikadharmakṣānti",
        "chinese": "無生法忍",
        "category": "Trí Tuệ & Quả Vị",
        "brief": "Tâm trí an định, thấu suốt và vững vàng trước sự thật rằng muôn pháp vốn không sanh, không diệt.",
        "detail": "Chữ 'Nhẫn' ở đây là trí tuệ sâu sắc nhận chân và an trú tuyệt đối nơi thật tướng vô sanh của vạn pháp, không còn khởi tâm sợ hãi trước tánh Không hay dao động trước sanh tử."
    },
    {
        "id": "phuong-tien-thien-xao",
        "term": "Phương tiện thiện xảo",
        "sanskrit": "Upāyakauśalya",
        "chinese": "方便善巧",
        "category": "Bồ Tát Đạo",
        "brief": "Nghệ thuật giáo hóa tinh tế, linh hoạt của Bồ-tát dựa trên nền tảng trí tuệ Bát Nhã và lòng đại bi.",
        "detail": "Bát-nhã là trí tuệ soi thấu bản thể, còn Phương tiện là hành động cứu độ cụ thể. Kinh Đại Bát Nhã dạy: 'Trí tuệ mà không có phương tiện là trói buộc; trí tuệ đi kèm phương tiện thiện xảo là giải thoát'."
    },
    {
        "id": "a-lai-da-thuc",
        "term": "A-lại-da thức",
        "sanskrit": "Ālayavijñāna",
        "chinese": "阿賴耶識",
        "category": "Pháp Số & Giáo Lý",
        "brief": "Thức thứ tám (Tạng thức), kho tàng lưu giữ tất cả hạt giống (chủng tử) nghiệp thiện, ác và vô ký.",
        "detail": "Là nền tảng duy trì dòng luân hồi sanh tử. Khi hành giả dùng kiếm trí tuệ Bát Nhã chặt đứt chấp ngã, A-lại-da thức được chuyển hóa thành Đại Viên Cảnh Trí (trí sáng như gương báu)."
    },
    {
        "id": "ngu-uan",
        "term": "Ngũ uẩn",
        "sanskrit": "Pañcaskandha",
        "chinese": "五蘊",
        "category": "Pháp Số & Giáo Lý",
        "brief": "Năm nhóm yếu tố cấu thành nên thân tâm của con người: Sắc, Thọ, Tưởng, Hành, Thức.",
        "detail": "Sắc là phần vật chất; Thọ là cảm giác; Tưởng là tri giác/tưởng tượng; Hành là ý chí/tâm lý tạo tác; Thức là nhận thức phân biệt. Quán soi năm uẩn đều 'không' chính là cửa ngõ bước vào giải thoát theo Bát Nhã Tâm Kinh."
    },
    {
        "id": "thap-nhi-nhan-duyen",
        "term": "Thập nhị nhân duyên",
        "sanskrit": "Dvādaśāṅgapratītyasamutpāda",
        "chinese": "十二因緣",
        "category": "Pháp Số & Giáo Lý",
        "brief": "Chuỗi mười hai mắt xích duyên khởi giải thích vòng luân hồi sinh tử của chúng sanh.",
        "detail": "Bắt đầu từ Vô minh ➔ Hành ➔ Thức ➔ Danh sắc ➔ Lục nhập ➔ Xúc ➔ Thọ ➔ Ái ➔ Thủ ➔ Hữu ➔ Sanh ➔ Lão tử. Bát Nhã quán soi: 'Không có vô minh, cũng không có hết vô minh; cho đến không có già chết, cũng không có hết già chết'."
    },
    {
        "id": "nhi-de",
        "term": "Nhị đế",
        "sanskrit": "Satyadvaya",
        "chinese": "二諦",
        "category": "Triết học Bát Nhã",
        "brief": "Hai tầng sự thật của đạo Phật: Tục đế (chân lý thế tục ước định) và Chân đế (chân lý cứu cánh tuyệt đối).",
        "detail": "Tục đế chấp nhận sự tồn tại nhân quả duyên sinh trên phương diện thế tục. Chân đế thấy rõ mọi pháp đều không có tự tánh rốt ráo. Người hiểu được Nhị đế thì không rơi vào chấp thường (hữu) cũng không rơi vào chấp đoạn (vô)."
    },
    {
        "id": "luc-ba-la-mat",
        "term": "Lục độ (Lục Ba-la-mật)",
        "sanskrit": "Ṣaṭpāramitā",
        "chinese": "六波羅蜜",
        "category": "Bồ Tát Đạo",
        "brief": "Sáu hạnh tu đưa qua bờ giác: Bố thí, Trì giới, Nhẫn nhục, Tinh tấn, Thiền định, Trí tuệ (Bát-nhã).",
        "detail": "Năm độ đầu như người mù, độ thứ sáu (Trí tuệ Bát-nhã) như đôi mắt dẫn đường. Có Bát-nhã soi đường thì bố thí không thấy có người cho, vật cho, người nhận (Tam luân không tịch)."
    },
    {
        "id": "tam-than",
        "term": "Tam thân Phật",
        "sanskrit": "Trikāya",
        "chinese": "三身",
        "category": "Trí Tuệ & Quả Vị",
        "brief": "Ba thân của Đức Phật: Pháp thân (thanh tịnh bản thể), Báo thân (phước đức trí tuệ), Hóa thân (ứng hiện độ sinh).",
        "detail": "Pháp thân chính là Chân Như tánh Không bất sinh bất diệt; Báo thân trang nghiêm ở cõi tịnh độ như Phật Lô-xá-na; Hóa thân tùy duyên thị hiện như Đức Phật Thích Ca nơi cõi Ta Bà."
    },
    {
        "id": "tam-muoi",
        "term": "Tam-muội (Tam-ma-địa)",
        "sanskrit": "Samādhi",
        "chinese": "三昧",
        "category": "Bồ Tát Đạo",
        "brief": "Trạng thái định tâm sâu lắng, an định tuyệt đối nơi chánh pháp, không bị cảnh giới dao động.",
        "detail": "Trong Kinh Đại Bát Nhã, Đức Phật và chư Đại Bồ Tát thường nhập vô lượng Tam-muội (như Hải ấn tam muội, Kim cang tam muội) trước khi phóng quang thuyết pháp thâm sâu."
    },
    {
        "id": "da-la-ni",
        "term": "Đà-la-ni",
        "sanskrit": "Dhāraṇī",
        "chinese": "陀羅尼",
        "category": "Bồ Tát Đạo",
        "brief": "Tổng trì; năng lực thâu tóm vô lượng pháp nghĩa, ghi nhớ không quên và ngăn chặn mọi điều ác.",
        "detail": "Hành giả Bát Nhã đắc Đà-la-ni có khả năng ghi nhớ toàn bộ kinh văn giáo pháp chư Phật dạy, đồng thời hộ trì tâm ý luôn an trú nơi chánh niệm thanh tịnh."
    },
    {
        "id": "kim-cuong-nang-doan",
        "term": "Kim Cương Năng Đoạn",
        "sanskrit": "Vajracchedikā",
        "chinese": "金剛能斷",
        "category": "Triết học Bát Nhã",
        "brief": "Tên gọi Hội thứ 9 của Kinh Đại Bát Nhã: Trí tuệ sắc bén, kiên cố như kim cương chém đứt mọi vọng hoặc chấp thủ.",
        "detail": "Kim cương có hai đặc tính: cứng rắn nhất không gì phá nổi, và sắc bén nhất có thể cắt đứt muôn vật. Trí tuệ Kim Cương Bát Nhã cắt đứt bốn tướng: Ngã tướng, Nhân tướng, Chúng sanh tướng và Thọ giả tướng."
    },
    {
        "id": "thien-hien",
        "term": "Thiện Hiện (Tu-bồ-đề)",
        "sanskrit": "Subhūti",
        "chinese": "善現 / 須菩提",
        "category": "Nhân Vật Kinh Điển",
        "brief": "Đại đệ tử đệ nhất Giải Không của Đức Thế Tôn, đương cơ thưa hỏi chính trong Kinh Đại Bát Nhã.",
        "detail": "Ngài Tu-bồ-đề được dịch nghĩa là Thiện Hiện hay Không Sanh. Trong suốt 600 Quyển Đại Bát Nhã, ngài là bậc thượng thủ được Đức Phật chỉ định đàm luận và xiển dương giáo nghĩa Bát Nhã thậm thâm."
    },
    {
        "id": "man-thu-that-loi",
        "term": "Mạn-thù-thất-lợi (Văn Thù)",
        "sanskrit": "Mañjuśrī",
        "chinese": "曼殊室利 / 文殊師利",
        "category": "Nhân Vật Kinh Điển",
        "brief": "Đại Trí Văn Thù Sư Lợi Bồ Tát, biểu trưng cho trí tuệ căn bản vô phân biệt của Phật giáo Đại thừa.",
        "detail": "Hội thứ 7 của Kinh Đại Bát Nhã mang tên ngài (Văn Thù Sư Lợi Bát Nhã). Ngài cưỡi sư tử xanh, tay cầm kiếm báu trí tuệ chém tan lưới si ám của chúng sanh."
    },
    {
        "id": "xa-loi-tu",
        "term": "Xá-lợi Tử (Xá-lợi-phất)",
        "sanskrit": "Śāriputra",
        "chinese": "舍利子 / 舍利弗",
        "category": "Nhân Vật Kinh Điển",
        "brief": "Đại đệ tử đệ nhất Trí Tuệ của Đức Phật, đại diện cho trí tuệ tối cao của hàng Thanh văn trong hội Bát Nhã.",
        "detail": "Trong Bát Nhã Ba La Mật Đa Tâm Kinh, Đức Quán Tự Tại Bồ Tát đã xưng hô 'Này Xá-lợi Tử' để khai thị giáo nghĩa 'Sắc bất dị không, không bất dị sắc'."
    },
    {
        "id": "vo-vi-phap",
        "term": "Vô vi pháp",
        "sanskrit": "Asaṃskṛta-dharma",
        "chinese": "無為法",
        "category": "Triết học Bát Nhã",
        "brief": "Các pháp không do duyên tạo tác, không sanh, không trụ, không diệt, bản nhiên tịch tịnh.",
        "detail": "Trái ngược với Hữu vi pháp (các pháp do nhân duyên tạo nên có sanh diệt), Vô vi pháp là thực tại tối hậu, tịch tịnh, chỉ trạng thái giải thoát thanh tịnh của Niết-bàn."
    },
    {
        "id": "huu-vi-phap",
        "term": "Hữu vi pháp",
        "sanskrit": "Saṃskṛta-dharma",
        "chinese": "有為法",
        "category": "Triết học Bát Nhã",
        "brief": "Tất cả các hiện tượng do nhân duyên tạo tác, có sinh, có trụ, có dị, có diệt.",
        "detail": "Kinh Kim Cương dạy: 'Nhất thiết hữu vi pháp, Như mộng, huyễn, bào, ảnh, Như lộ diệc như điện, Ưng tác như thị quán'. Thấy rõ bản chất mong manh của hữu vi pháp là bước đầu của trí tuệ."
    },
    {
        "id": "tam-giai-thoat-mon",
        "term": "Tam giải thoát môn",
        "sanskrit": "Trīṇi vimokṣamukhāni",
        "chinese": "三解脫門",
        "category": "Triết học Bát Nhã",
        "brief": "Ba cánh cửa bước vào cảnh giới giải thoát Niết-bàn: Không, Vô tướng, Vô nguyện (Vô tác).",
        "detail": "Không môn: thấy vạn pháp do duyên sinh không có tự tánh; Vô tướng môn: lìa mọi tướng trạng giả dối sai biệt; Vô nguyện môn: tâm không còn mong cầu hay vướng mắc vào bất kỳ cõi giới sinh diệt nào."
    },
    {
        "id": "bat-nhi-phap-mon",
        "term": "Bất nhị pháp môn",
        "sanskrit": "Advaya-dharmamukha",
        "chinese": "不二法門",
        "category": "Triết học Bát Nhã",
        "brief": "Cửa pháp siêu việt nhị nguyên phân biệt: không kẹt vào hai bên như có - không, sanh - tử, nhơ - sạch.",
        "detail": "Kinh Duy-ma-cật và Bát Nhã đều xiển dương: thật tướng của pháp giới vốn bình đẳng tuyệt đối, vượt ra ngoài mọi cặp phạm trù đối đãi như tốt - xấu, phàm - thánh, phiền não - bồ đề."
    },
    {
        "id": "tu-dieu-de",
        "term": "Tứ diệu đế",
        "sanskrit": "Caturāryasatya",
        "chinese": "四妙諦",
        "category": "Pháp Số & Giáo Lý",
        "brief": "Bốn sự thật mầu nhiệm cao quý do Đức Phật tuyên thuyết: Khổ đế, Tập đế, Diệt đế, Đạo đế.",
        "detail": "Khổ đế: sự thật về khổ đau; Tập đế: nguyên nhân sinh khổ (tham ái, si mê); Diệt đế: sự tịch diệt của khổ đau (Niết-bàn); Đạo đế: con đường đưa đến dứt khổ (Bát Chánh Đạo). Bát Nhã soi chiếu: 'Không có khổ, tập, diệt, đạo'."
    },
    {
        "id": "bat-chanh-dao",
        "term": "Bát chánh đạo",
        "sanskrit": "Āryāṣṭāṅgamārga",
        "chinese": "八正道",
        "category": "Pháp Số & Giáo Lý",
        "brief": "Con đường tám nhánh chân chánh: Chánh kiến, Chánh tư duy, Chánh ngữ, Chánh nghiệp, Chánh mạng, Chánh tinh tấn, Chánh niệm, Chánh định.",
        "detail": "Là cốt lõi của Đạo đế. Trong tinh thần Bát Nhã, Bát Chánh Đạo được thực hành với tâm 'vô sở đắc', nghĩa là đi trên đường chánh mà không thấy có đường để đi hay người đi, an nhiên giải thoát."
    },
    {
        "id": "tu-vo-luong-tam",
        "term": "Tứ vô lượng tâm",
        "sanskrit": "Caturbrahmavihāra",
        "chinese": "四無量心",
        "category": "Bồ Tát Đạo",
        "brief": "Bốn tâm lượng rộng lớn vô bờ của Bồ-tát: Từ (ban vui), Bi (cứu khổ), Hỷ (vui theo điều lành), Xả (buông bỏ phân biệt).",
        "detail": "Bồ-tát hành Bát Nhã phát khởi Tứ vô lượng tâm trùm khắp mười phương pháp giới, cứu độ cùng khắp chúng sanh mà tâm vẫn như hư không, không thấy có tướng chúng sanh để xả hay không xả."
    },
    {
        "id": "luc-thong",
        "term": "Lục thông",
        "sanskrit": "Ṣaḍabhijñā",
        "chinese": "六通",
        "category": "Trí Tuệ & Quả Vị",
        "brief": "Sáu phép thần thông thanh tịnh: Thiên nhãn thông, Thiên nhĩ thông, Tha tâm thông, Túc mạng thông, Thần túc thông, Lậu tận thông.",
        "detail": "Năm thông đầu tiên ngoại đạo cũng có thể đắc qua thiền định, nhưng Lậu tận thông (dứt sạch mọi phiền não lậu hoặc) chỉ có được nhờ ngọn đuốc trí tuệ Bát-nhã soi rọi."
    },
    {
        "id": "thap-luc",
        "term": "Thập lực",
        "sanskrit": "Daśabalāni",
        "chinese": "十力",
        "category": "Trí Tuệ & Quả Vị",
        "brief": "Mười năng lực trí tuệ vô úy đặc biệt chỉ riêng Đức Phật mới thành tựu trọn vẹn.",
        "detail": "Bao gồm: Trí biết chỗ đúng chỗ sai (Thị xứ phi xứ trí lực), Trí biết nghiệp báo ba đời, Trí biết căn cơ chúng sanh, Trí biết các cõi giới, v.v., đều xuất phát từ biển trí tuệ Tát-bà-nhã."
    },
    {
        "id": "phap-than",
        "term": "Pháp thân",
        "sanskrit": "Dharmakāya",
        "chinese": "法身",
        "category": "Trí Tuệ & Quả Vị",
        "brief": "Thân chân thật bản nhiên của Phật, đồng nhất với Chân Như và Tánh Không khắp pháp giới.",
        "detail": "Kinh Kim Cương dạy: 'Nhược dĩ sắc kiến ngã, Dĩ âm thanh cầu ngã, Thị nhân hành tà đạo, Bất năng kiến Như Lai'. Thấy được thực tướng tánh Không của vạn pháp chính là diện kiến Pháp thân Phật."
    },
    {
        "id": "niem-ban",
        "term": "Niết-bàn",
        "sanskrit": "Nirvāṇa",
        "chinese": "涅槃",
        "category": "Trí Tuệ & Quả Vị",
        "brief": "Trạng thái tịch tịnh, dập tắt hoàn toàn mọi ngọn lửa tham sân si phiền não và sanh tử luân hồi.",
        "detail": "Bát Nhã nhìn nhận: 'Sanh tử tức Niết-bàn'. Khi tâm dứt sạch vọng niệm phân biệt và ngã chấp thì ngay nơi thân năm uẩn này hiện tiền là Niết-bàn thanh tịnh an lạc."
    }
]

def build_glossary():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(repo_root, 'reader', 'data', 'glossary.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(GLOSSARY_TERMS, f, ensure_ascii=False, indent=2)
        
    print(f"Generated glossary with {len(GLOSSARY_TERMS)} authoritative terms at {out_path}")

if __name__ == '__main__':
    build_glossary()

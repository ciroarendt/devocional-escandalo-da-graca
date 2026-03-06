#!/usr/bin/env python3
"""
Patch devotionals.js: replace January (days 1-31) with expanded versions.
"""
import json

JANUARY_NEW = [
    {
        "day": 1, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Deus Não Existe — Ele É",
        "verse_text": "Disse Deus a Moisés: EU SOU O QUE SOU. Assim dirás aos filhos de Israel: EU SOU me enviou a vós.",
        "verse_ref": "Êxodo 3:14",
        "paragraphs": [
            "Há uma distinção radical que precisa ser resgatada antes de tudo: Deus não existe — Ele É. Existir implica ter começado em algum momento, ter sido gerado por algo maior. Deus jamais começou. Ele simplesmente É, antes de todo começo, além de toda categoria, sustentando toda realidade com a força de Sua presença.",
            "Quando Moisés, diante da sarça ardente, perguntou o nome de Deus, a resposta foi a mais desconcertante da história: 'EU SOU O QUE SOU.' Não um título, não uma função, não uma descrição. Apenas o puro ser. Deus não se define porque o que se define se limita — e Ele é ilimitado em todos os sentidos que a linguagem humana ainda não inventou.",
            "O que torna Deus verdadeiramente Deus é exatamente isso: Ele é anterior a tudo. Antes que as estrelas fossem lançadas no espaço, antes que o primeiro átomo vibrasse, antes que o conceito de 'antes' fizesse qualquer sentido — Ele já Era. É a divindade em pessoa: incomparável, irresistível, imortal, imutável, invencível.",
            "Essa compreensão não é apenas teológica — ela é transformadora. Não estamos buscando um Deus que precisa ser localizado ou convencido. Ele está nas profundezas dos oceanos e nas extremidades do universo. É a expressão do ar que respiramos, o fundamento invisível de toda matéria. Está em tudo e é mais que tudo.",
            "A religião frequentemente nos ensina a buscar a Deus como quem procura algo perdido. Mas o 'EU SOU' não se perde. Ele é a própria estrutura da realidade. Buscar a Deus não é sair em uma expedição — é acordar para o que sempre esteve presente.",
            "Ao iniciar esta jornada de 365 dias, deixe que essa verdade fundamente tudo o mais. Você não está descobrindo um Deus novo — está sendo apresentado a Quem sempre foi, sempre é e sempre será. Este Deus eterno escolheu se revelar a você pessoalmente.",
            "Descanse nessa realidade: o mesmo Deus que respondeu a Moisés da sarça ardente é o Deus que habita em você hoje pelo Espírito. O 'EU SOU' vive dentro de você. Essa é a mais escandalosa das verdades cristãs — e é onde tudo começa."
        ],
        "references": ["João 1:1-3", "Colossenses 1:17", "Atos 17:28", "Apocalipse 1:8", "Isaías 44:6"],
        "prayer": "Eu declaro que Tu és o EU SOU — não apenas um ser no universo, mas a origem e o fundamento de toda existência. Eu sei que antes de tudo existir, Tu já eras; e antes que eu nascesse, Tu já me conhecias pelo nome. Eu afirmo que essa jornada de 365 dias é uma imersão em Quem Tu és, e que ao final dela serei irremediavelmente transformado pela revelação do Teu ser eterno.",
        "month_num": 1, "day_of_month": 1, "date_label": "1 de Janeiro"
    },
    {
        "day": 2, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Antes de Tudo, o Verbo Já Era",
        "verse_text": "No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus.",
        "verse_ref": "João 1:1",
        "paragraphs": [
            "João abre seu evangelho com uma afirmação que rompe todas as categorias filosóficas: 'No princípio era o Verbo.' Não 'surgiu', não 'foi criado', não 'apareceu' — era. O ser de Cristo é anterior ao próprio princípio. Antes de qualquer começo, Ele já existia em plena e perfeita comunhão com o Pai.",
            "A criação é infinita, mas Deus é eterno. O infinito tem começo mas não tem fim. O eterno não tem nem começo nem fim. Essa distinção é capital: o universo é imensuravelmente vasto, mas teve uma origem. Deus não. Ele habita além das fronteiras do que chamamos de tempo e espaço.",
            "Jesus — o Verbo encarnado — estava com Deus antes de todas as coisas. O plano da redenção não foi uma solução de emergência que Deus inventou depois da queda de Adão. Era uma decisão tomada na eternidade, antes que qualquer coisa fosse criada. Você estava no coração desse plano antes de existir.",
            "Quando olhamos para a eternidade de Deus, descobrimos que Sua relação conosco não começou no dia em que nascemos nem no dia em que nos convertemos. Ele nos conhecia antes da fundação do mundo, nos escolheu antes mesmo de existirmos, nos amou com amor eterno antes de qualquer decisão nossa.",
            "Isso significa que Deus não leva em conta apenas os poucos anos que você viveu. Ele considera toda a história desde o princípio, porque tudo foi planejado com um propósito que inclui você desde antes da criação. Você é parte de um projeto eterno, não de uma improvisação temporal.",
            "Que consolo profundo saber que não somos fruto do acaso! O Deus que existia antes de tudo pensou em você antes de criar o mundo. Sua existência é a manifestação temporal de um plano eterno, tecido com amor antes que o tempo tivesse sentido.",
            "Viva hoje com a consciência de que você é eterno no plano de Deus. Os problemas que enfrenta têm prazo de validade. O amor de Deus por você — esse não tem começo nem fim."
        ],
        "references": ["Efésios 1:4", "Colossenses 1:15-17", "Hebreus 1:2-3", "Provérbios 8:22-31", "1 Pedro 1:20"],
        "prayer": "Eu declaro que sou parte de um plano eterno traçado antes da fundação do mundo, e que o Verbo que era antes de tudo é o mesmo que habita em mim hoje. Eu sei que o Deus eterno não pensa em mim apenas em termos de minha vida breve — Ele me vê pela eternidade. Eu afirmo que minha vida tem peso eterno e que cada dia vivido em comunhão com o Pai é mais um capítulo de uma história que começou antes do tempo.",
        "month_num": 1, "day_of_month": 2, "date_label": "2 de Janeiro"
    },
    {
        "day": 3, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "O Marco Zero — A Criação Foi Para Você",
        "verse_text": "No princípio, Deus criou os céus e a terra.",
        "verse_ref": "Gênesis 1:1",
        "paragraphs": [
            "O primeiro grande marco da história humana é a Criação. Antes que qualquer homem existisse, Deus criou o ambiente perfeito. Não por acaso, não por necessidade — por amor. Ele preparou um lar antes de trazer o filho para dentro dele.",
            "Pense nisso: Deus não criou o ser humano e depois pensou onde colocá-lo. Ele pensou no ser humano primeiro, planejou tudo o que esse ser precisaria para florescer e, somente então, criou o mundo. Você foi a motivação da criação — não um resultado tardio.",
            "A maçã que cai do galho não foi criada para o galho, mas para você. A fonte de água cristalina não foi criada para encher o rio, mas para satisfazer sua sede. O sol não foi posicionado para ornar o universo — foi posicionado para aquecer sua pele, fazer suas plantas crescerem, governar seu ritmo de vida.",
            "Já parou para pensar no quanto você importa para o cosmos? Em você toda a criação encontra seu sentido mais profundo. O ser humano é a coroa da obra de Deus — não porque merecemos, mas porque fomos feitos como portadores da imagem do Criador em um mundo criado.",
            "Isso muda radicalmente sua relação com a natureza e com Deus. Você não é um habitante aleatório de um planeta insignificante em uma galáxia entre bilhões. Você é o destinatário de um projeto que envolveu a criação inteira.",
            "Quando você sai de manhã e sente o sol no rosto, lembre: foi planejado para você. Quando come um prato de comida, lembre: a terra foi fértil para você. Quando respira, lembre: o ar foi composto com precisão para você.",
            "Viva com essa consciência. Você não é um acidente cósmico — é o objeto do amor mais criativo e extravagante que o universo já conheceu. A criação inteira declara a sua importância para o coração de Deus."
        ],
        "references": ["Gênesis 1:26-28", "Salmos 8:3-6", "Salmos 19:1", "Romanos 1:20", "Tiago 1:17"],
        "prayer": "Eu declaro que fui o propósito da criação — que cada maravilha deste mundo foi preparada pelo Pai como expressão de amor por mim e por toda a humanidade. Eu sei que não sou acidente nem sobra de um universo indiferente, mas filho amado de um Pai que preparou tudo antes de me chamar à existência. Eu afirmo que vivo com gratidão profunda por cada detalhe da criação, reconhecendo nele a assinatura do Deus que me amou antes de me criar.",
        "month_num": 1, "day_of_month": 3, "date_label": "3 de Janeiro"
    },
    {
        "day": 4, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Jesus Rachou a História ao Meio",
        "verse_text": "Vindo a plenitude dos tempos, Deus enviou seu Filho, nascido de mulher, nascido sob a lei.",
        "verse_ref": "Gálatas 4:4",
        "paragraphs": [
            "O segundo marco zero da história é o nascimento de Jesus. Hoje, ao redor do mundo inteiro, alguém está assinando um documento e registrando uma data que existe porque Jesus de Nazaré nasceu. Nenhum filósofo, rei, imperador ou conquistador fez isso — apenas Jesus.",
            "Alexandre, o Grande, conquistou o mundo com exércitos e espadas, mas o mundo esqueceu suas datas. Napoleão dominou continentes, mas seu calendário não sobreviveu. Jesus não pegou em armas, não liderou batalhas, não acumulou riquezas — e ainda assim dividiu a história humana em duas partes.",
            "Antes de Cristo e depois de Cristo. Assim o mundo inteiro conta o tempo. Essa é a evidência mais concreta de que houve algo absolutamente único naquele carpinteiro de Nazaré. Ele não apenas viveu — Ele mudou o eixo da história.",
            "E o mais extraordinário: Jesus ressuscitou. Não metaforicamente, não simbolicamente — corporalmente. O homem que comprovadamente morreu numa cruz romana voltou a viver três dias depois. Esse fato ainda hoje movimenta nações, inspira curas, transforma vidas, derruba impérios de mentira.",
            "A vinda de Cristo na plenitude dos tempos foi a intervenção mais radical que Deus já fez no mundo. Não enviou um representante, uma mensagem, um anjo — Ele mesmo veio. Tomou carne, viveu entre nós, sofreu o que sofremos, morreu como morremos — e depois desfez a morte.",
            "Você está do lado certo da história. Do lado certo da cruz, do túmulo vazio, da ressurreição. Os profetas do Antigo Testamento anunciaram este momento e morreram sem vê-lo. Você vive com o cumprimento em mãos.",
            "Toda vez que você escreve a data de hoje, está inscrevendo na história um testemunho do segundo marco zero. Jesus de Nazaré existiu, viveu, morreu e ressuscitou. E isso mudou tudo — inclusive você."
        ],
        "references": ["Lucas 2:10-11", "João 1:14", "Filipenses 2:6-8", "Hebreus 1:1-3", "Mateus 1:23"],
        "prayer": "Eu declaro que estou do lado certo da história — do lado da ressurreição, da graça e do Reino de Deus estabelecido em Cristo Jesus. Eu sei que o mesmo Jesus que rachou a história ao meio é o mesmo que vive em mim hoje, e que Seu poder não é histórico mas eternamente presente. Eu afirmo que minha vida tem um antes e um depois — o momento em que encontrei o ressuscitado — e que nada mais será como era.",
        "month_num": 1, "day_of_month": 4, "date_label": "4 de Janeiro"
    },
    {
        "day": 5, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Seu Nascimento É um Marco Eterno",
        "verse_text": "Pois Tu formaste o meu interior, Tu me teceste no ventre de minha mãe. Eu Te louvo porque me fizeste de modo especial e admirável.",
        "verse_ref": "Salmos 139:13-14",
        "paragraphs": [
            "O terceiro marco zero é o dia do seu nascimento. Naquele dia, o propósito eterno de Deus ganhou expressão temporal. Você não entrou no mundo por acidente biológico — você foi convocado do ventre da eternidade para existir neste exato ponto da história.",
            "Mais de 60 bilhões de seres humanos já permearam a Terra, e dentre eles, aproximadamente 8 bilhões existem hoje. Mas nenhum deles é você. Você é único, insubstituível, portador de uma combinação de dons, chamados e propósitos que mais ninguém no mundo carrega.",
            "Deus se relaciona com você considerando os três marcos zero: a criação do mundo que preparou seu lar, a vinda de Cristo que restaurou sua posição, e o seu nascimento que concretizou no tempo o que foi planejado na eternidade. Sua existência é o ponto de convergência desses três marcos.",
            "O salmista foi tomado de louvor quando percebeu que Deus o teceu no ventre de sua mãe. Não foi a mãe biológica quem fez isso — ela foi apenas o instrumento. O artesão era Deus, e Ele trabalhou com precisão infinita, conhecendo cada detalhe do que você seria.",
            "Cada dia da sua vida é uma página de uma história que começou antes do tempo. As dificuldades que enfrentou, as alegrias que viveu, as pessoas que cruzaram seu caminho — tudo foi tecido dentro de um propósito maior que você ainda está descobrindo.",
            "Você foi pensado na eternidade, preparado na criação, resgatado na cruz, e manifestado no dia do seu nascimento. Cada fase dessa história revela o cuidado extravagante de um Pai que não deixa nenhum detalhe ao acaso.",
            "Celebre sua existência com gratidão profunda. Você é mais do que seu currículo, suas conquistas ou seus fracassos. Você é a manifestação temporal de um plano eterno que o céu inteiro festejou no dia em que você nasceu."
        ],
        "references": ["Jeremias 1:5", "Salmos 139:15-16", "Isaías 49:1", "Efésios 2:10", "Gálatas 1:15"],
        "prayer": "Eu declaro que meu nascimento não foi acidente, mas convocação — que fui trazido ao mundo neste momento exato da história porque Deus tinha um propósito específico que só eu poderia cumprir. Eu sei que fui tecido com precisão no ventre de minha mãe pelas mãos do Criador, que me conhecia pelo nome antes que eu tivesse nome. Eu afirmo que cada dia de vida é um presente, e que vivo com consciência plena da grandeza do propósito que o Pai depositou em mim.",
        "month_num": 1, "day_of_month": 5, "date_label": "5 de Janeiro"
    },
    {
        "day": 6, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Nascer de Novo É Mudar de Natureza",
        "verse_text": "Se alguém não nascer de novo, não pode ver o reino de Deus.",
        "verse_ref": "João 3:3",
        "paragraphs": [
            "Nicodemos era tudo que o sistema religioso valoriza: culto, experiente, bem relacionado, doutor em Escrituras, autoridade do Sinédrio. E Jesus, ao encontrá-lo, cortou toda a conversa teológica com uma frase que ninguém esperava: 'Importa nascer de novo.'",
            "Não era sobre aprender mais, se esforçar mais, ser mais piedoso. Era sobre uma transformação de natureza — algo que nenhum esforço humano pode produzir. Nasce de novo quem recebe do Espírito, não quem se disciplina pela carne.",
            "Nicodemos ficou desconcertado. Como pode um homem adulto nascer outra vez? Jesus não estava falando de biologia — estava falando de ontologia. Não era sobre o que você faz, mas sobre quem você é. Uma nova natureza, uma nova identidade, um novo status diante de Deus.",
            "O que é nascido da carne é carne. O que é nascido do Espírito é espírito. Nascer de novo não é melhorar a versão antiga — é receber uma natureza completamente diferente. É a diferença entre reformar uma casa velha e receber um palácio novo.",
            "Esse mistério ainda está na cabeça de milhões de pessoas dentro das igrejas. Muitos conhecem a Bíblia de capa a capa, praticam rituais com perfeição, frequentam cultos há décadas — mas nunca experimentaram o novo nascimento que transforma de dentro para fora.",
            "Nascer de novo é o momento em que o 'EU SOU' — esse Deus que simplesmente É — passa a habitar em você. Você não apenas acredita em Deus: você passa a portar Deus dentro de si. Isso muda tudo.",
            "Hoje, reflita sobre sua própria experiência do novo nascimento. Não como um evento do passado que você recita, mas como uma realidade viva que define quem você é agora. Você não é apenas uma pessoa religiosa — é uma nova criação."
        ],
        "references": ["João 3:5-8", "2 Coríntios 5:17", "1 Pedro 1:23", "João 1:12-13", "Tito 3:5"],
        "prayer": "Eu declaro que sou uma nova criação em Cristo Jesus — que o que nasceu do Espírito em mim é espírito, e essa natureza nova é mais real e mais poderosa que qualquer herança da carne. Eu sei que não fui apenas melhorado pela religião, mas transformado pela graça, e que o novo nascimento em mim é uma obra de Deus que nenhuma circunstância pode desfazer. Eu afirmo que vivo da identidade de filho, não do esforço de um servo tentando provar algo.",
        "month_num": 1, "day_of_month": 6, "date_label": "6 de Janeiro"
    },
    {
        "day": 7, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Deus É Mais Real Que o Visível",
        "verse_text": "Aquele que não ama não conhece a Deus, porque Deus é amor.",
        "verse_ref": "1 João 4:8",
        "paragraphs": [
            "O objetivo de nossa fé não é comprovar que Deus existe, como se precisássemos de um argumento intelectual vencedor. O objetivo é descobrir que Deus é mais real do que qualquer coisa que nossos olhos jamais verão. A realidade de Deus não precisa de prova — precisa de revelação.",
            "Os ateus dizem: 'Se Deus existe, por que não o vemos?' Mas as coisas mais reais da vida são invisíveis: amor, esperança, paz, propósito. Ninguém jamais viu o amor com os olhos, mas ninguém duvida de sua realidade quando o experimenta.",
            "A gravidade não pode ser fotografada, mas sustenta você no chão agora mesmo. O vento não tem forma visível, mas move oceanos e dobra florestas. Assim é Deus: invisível aos olhos físicos, irresistível à experiência da alma.",
            "O salmista orou: 'Ensina-nos a contar os nossos dias, para que alcancemos coração sábio.' Contar os dias não é planejar a agenda — é somar à sua vida todos os fatos e evidências de Deus na história antes de você nascer. Quando você faz isso, não há como negar Sua realidade.",
            "Deus é amor — não apenas que Ele ama, mas que Ele É amor. Não é uma qualidade que Ele possui; é Sua essência. E você experimenta Deus toda vez que experimenta amor genuíno, bondade gratuita, beleza inesperada.",
            "Quando soma à sua existência os marcos da criação, de Cristo e do seu nascimento, percebe que a realidade de Deus não é teoria filosófica — é a base concreta de toda a sua existência. Você não estaria aqui se Deus não fosse real.",
            "Vá além da crença intelectual e experimente a realidade de Deus. Não se trata apenas de acreditar que Ele existe — se trata de viver dentro da consciência de que Ele É, e que você existe dentro d'Ele."
        ],
        "references": ["Salmos 90:12", "Romanos 1:19-20", "Hebreus 11:6", "Atos 17:27-28", "Salmos 34:8"],
        "prayer": "Eu declaro que a realidade de Deus é mais sólida e mais concreta do que qualquer coisa que meus olhos físicos podem ver, e que vivo dentro d'Ele como o peixe vive dentro do mar. Eu sei que cada ato de amor genuíno que experimento é uma evidência tangível de que Deus É amor, e que estou cercado por Sua presença em cada momento. Eu afirmo que a minha fé não é esforço intelectual para acreditar no invisível, mas rendição gozosa a Quem me sustenta e me habita.",
        "month_num": 1, "day_of_month": 7, "date_label": "7 de Janeiro"
    },
    {
        "day": 8, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Você Nasceu na Melhor Era da História",
        "verse_text": "Quando chegou a plenitude do tempo, Deus enviou o seu Filho.",
        "verse_ref": "Gálatas 4:4",
        "paragraphs": [
            "Precisamos discernir os dias em que vivemos e entender a era que nos foi dada. Vivemos nos melhores dias que a humanidade já conheceu — não porque a tecnologia avançou, não porque o mundo ficou mais pacífico, mas porque estamos do lado certo da cruz. Do lado do cumprimento.",
            "Os profetas de Israel anunciaram com precisão impressionante o que estava por vir: o Messias, o Reino, a nova aliança, o derramamento do Espírito. Eles viram de longe e anunciaram com fogo. Mas morreram sem ver o cumprimento. Nós nascemos no tempo do cumprimento.",
            "Muito da fé que é praticada hoje, porém, está descontextualizada. Oramos como se ainda estivéssemos na era dos profetas esperando o Messias. Vivemos como se a cruz ainda não tivesse acontecido. Pedimos coisas que já foram concedidas, como se Deus ainda estivesse processando o pedido.",
            "Assim como um casamento confere ao cônjuge um novo status social — herdeiro, parceiro, pertencente à nova família — a redenção em Cristo nos conferiu um novo status espiritual que precisa ser compreendido e vivido. Você não é mais o que era antes da cruz.",
            "Este é o tempo de atualizar nossa compreensão. A fé plenamente contextualizada não espera que Deus faça algo — declara e vive o que Ele já fez. Não pede o que já foi dado — agradece e usa o que já foi concedido.",
            "Você não está esperando a plenitude dos tempos — você vive nela. Não está esperando a vinda do Espírito — Ele já habita em você. Não está esperando a reconciliação com Deus — ela já foi feita em Cristo.",
            "Desperte para a grandeza do tempo em que você nasceu. Você tem acesso ao que reis e profetas desejaram e não viram. Viva à altura do privilégio da sua era."
        ],
        "references": ["Hebreus 1:1-2", "2 Coríntios 6:2", "Efésios 1:10", "Atos 2:17", "Hebreus 9:26"],
        "prayer": "Eu declaro que nasci na melhor era da história — no lado do cumprimento, com o Espírito habitando em mim e todas as promessas de Deus prontas em Cristo. Eu sei que os profetas anunciaram o que eu vivo, e que tenho acesso ao que eles apenas contemplaram de longe. Eu afirmo que vivo com o pleno privilégio desta era, operando na consciência do que foi consumado na cruz e confirmado na ressurreição.",
        "month_num": 1, "day_of_month": 8, "date_label": "8 de Janeiro"
    },
    {
        "day": 9, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Quatro Valores Que Mudam Tudo",
        "verse_text": "Se pela transgressão de um só a morte reinou, muito mais os que recebem a provisão da graça e a dádiva da justiça reinarão em vida.",
        "verse_ref": "Romanos 5:17",
        "paragraphs": [
            "Existem quatro valores fundamentais que estruturam toda a experiência da vida em Cristo: Graça, Justiça, Herança e Glória. Não são dogmas inventados pela tradição religiosa — são realidades eternas reveladas nas Escrituras que sempre estiveram ali, esperando serem compreendidas e vividas.",
            "Esses quatro valores não são apenas conceitos teológicos para serem estudados — são dimensões de uma realidade presente que o crente pode e deve habitar agora. São os quatro pilares do que significa reinar em vida.",
            "Graça é o ponto de partida de tudo. Não é apenas o perdão de pecados — é a perspectiva de Deus sobre você, o modo como Ele olha para você através de Cristo. É o favor imerecido que se tornou a base da nova existência.",
            "Justiça é o que Deus faz em você e por você através da graça. Não é sua justiça conquistada pelo esforço — é a justiça de Deus imputada a você, que te coloca em posição de filho aceito, sem acusação, diante do Pai.",
            "Herança é o que você recebe como filho de Deus — não como recompensa pelo desempenho, mas como legado da filiação. Tudo o que o Pai tem, pertence ao filho. Essa é a promessa extravagante da nova aliança.",
            "Glória é o destino e ao mesmo tempo o presente — a vida em sua dimensão mais plena, o brilho do caráter de Deus sendo refletido em você, o cumprimento do propósito para o qual você foi criado.",
            "Nos próximos meses desta jornada de 365 dias, mergulharemos em cada um desses valores. Prepare-se para uma transformação que vai muito além da religião — é uma revolução de identidade."
        ],
        "references": ["Romanos 5:17", "Romanos 14:17", "Efésios 1:3", "2 Pedro 1:3", "Colossenses 1:12-13"],
        "prayer": "Eu declaro que fui feito para reinar em vida — que a graça, a justiça, a herança e a glória não são promessas futuras, mas realidades presentes que me foram conferidas em Cristo. Eu sei que Romanos 5:17 não é uma aspiração religiosa, mas uma declaração de fato sobre quem sou e o que tenho em Cristo agora mesmo. Eu afirmo que minha caminhada com Deus não é de um mendigo esperando favores, mas de um filho reinando na abundância da graça que me foi dada.",
        "month_num": 1, "day_of_month": 9, "date_label": "9 de Janeiro"
    },
    {
        "day": 10, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Reinar Em Vida — Agora, Não Depois",
        "verse_text": "Porque, se pela ofensa de um só a morte reinou, muito mais os que recebem a abundância da graça reinarão em vida por Jesus Cristo.",
        "verse_ref": "Romanos 5:17",
        "paragraphs": [
            "Por séculos, a Igreja foi catequizada a uma fé que adiava o melhor para depois da morte. 'Aguentar o sofrimento', 'pagar o preço', 'negar a si mesmo' — com a promessa de que um dia, no céu, tudo seria diferente. A intenção era pura. Mas o raciocínio estava equivocado.",
            "Provérbios 13:12 adverte: 'A esperança adiada adoece o coração.' Uma fé que só promete para o futuro inevitavelmente adoece o presente. E Deus não criou o ser humano para viver adoecido, esperando que a morte resolva o que a graça já resolveu.",
            "Se a vida abundante fosse exclusivamente para a eternidade, por que Deus criou Adão para viver na Terra? Por que Ele teria dado a Adão autoridade para governar a criação aqui? O propósito original era reinar em vida — aqui e agora, não apenas lá e depois.",
            "O versículo é inequívoco: 'reinarão em vida'. Não na morte, não no céu, não na eternidade — em vida. Agora. Hoje. No presente. A abundância da graça não é uma promessa escatológica — é uma realidade disponível para quem a recebe hoje.",
            "A proposta da redenção foi nos devolver o direito que Adão possuía: reinar sobre a criação como filhos de Deus, portadores de Sua imagem, governadores de Sua herança. A cruz não apenas nos salvou do inferno — nos restituiu ao jardim.",
            "Isso não é prosperidade superficial — é profundidade de identidade. Reinar em vida significa viver com autoridade espiritual, clareza de propósito, paz que excede o entendimento, e amor que não depende das circunstâncias.",
            "Você foi destinado para isso — não para depois da morte, mas para hoje. A questão é: você está vivendo no nível do seu destino?"
        ],
        "references": ["Provérbios 13:12", "Gênesis 1:28", "Apocalipse 1:6", "Romanos 8:37", "João 10:10"],
        "prayer": "Eu declaro que fui criado para reinar em vida — não depois da morte, não no céu distante, mas aqui, agora, neste dia. Eu sei que a abundância da graça que recebi não é uma promessa futura que aguardo com ansiedade, mas uma realidade presente que habito com consciência. Eu afirmo que recuso a mentalidade de sobrevivência religiosa e abraço a posição de herdeiro reinante que Cristo me restituiu.",
        "month_num": 1, "day_of_month": 10, "date_label": "10 de Janeiro"
    },
    {
        "day": 11, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "O Pai-Nosso Já Foi Completamente Respondido",
        "verse_text": "Está consumado!",
        "verse_ref": "João 19:30",
        "paragraphs": [
            "A oração mais recitada em todo o mundo cristão é o Pai-Nosso. Mas poucas pessoas percebem que essa oração já foi completamente respondida. Cada petição que ela contém foi cumprida em Cristo. É uma oração de realidades consumadas, não de esperanças ainda pendentes.",
            "Quando oramos 'Venha o Teu Reino', estamos dizendo que o Reino ainda não veio — mas Jesus declarou expressamente: 'O Reino de Deus está dentro de vós.' O Reino não está a caminho, está aqui. Está em você.",
            "Quando oramos 'Seja feita a Tua vontade assim na terra como no céu', estamos dizendo que a vontade de Deus ainda não está feita — mas Jesus, na cruz, declarou com a última força de sua voz: 'Está consumado.' Feito. Encerrado. Completado.",
            "Isso não significa parar de orar. Significa contextualizar a oração. Significa orar além das redundâncias — não ficar pedindo a Deus o que Ele já deu, não ficar pedindo o que Ele já fez. A oração madura declara verdades, não repete pedidos já respondidos.",
            "A função mais profunda da oração não é convencer Deus a agir. É revelar o Reino — colonizar corações e situações com a realidade de Deus, trazer o que é do céu para a terra, e manter a comunhão íntima entre o Pai e Seus filhos.",
            "Ore com a consciência de alguém que sabe o que já possui. Ore como filho que dialoga com o Pai, não como mendigo que implora por favores. A diferença na qualidade dessa experiência de oração é extraordinária.",
            "Quando você orar hoje, declare verdades ao invés de formular súplicas por coisas que já são suas. Essa postura transforma completamente a vida de oração e aprofunda a intimidade com Deus."
        ],
        "references": ["Lucas 17:21", "João 19:30", "Mateus 6:9-13", "1 Coríntios 3:16", "Lucas 11:1-4"],
        "prayer": "Eu declaro que o Pai-Nosso foi completamente respondido — que o Reino veio, que a vontade de Deus foi feita, que o consumado na cruz é minha realidade presente. Eu sei que o modelo de oração a que fui chamado não é o de um mendigo pedindo o que Deus ainda não decidiu, mas o de um filho que dialoga com o Pai na intimidade do que já foi feito. Eu afirmo que minha vida de oração é uma celebração de realidades consumadas, e que cada vez que oro, colonizo o mundo ao meu redor com a realidade do Reino.",
        "month_num": 1, "day_of_month": 11, "date_label": "11 de Janeiro"
    },
    {
        "day": 12, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Você Tem as Chaves — Não Precisa Bater",
        "verse_text": "Eu te darei as chaves do Reino dos céus; o que você ligar na terra terá sido ligado nos céus.",
        "verse_ref": "Mateus 16:19",
        "paragraphs": [
            "Antes da cruz, o modelo de operação espiritual era do céu para a terra: Deus iniciava, os homens respondiam. Os profetas recebiam palavra, os reis aguardavam instrução, os sacerdotes intercediam como mediadores entre o povo e Deus.",
            "Mas depois da cruz e da ressurreição, Jesus anunciou uma mudança radical de modelo. Ele disse a Pedro: 'Eu te darei as chaves do Reino dos céus.' Chaves. Não uma senha de acesso, não um pedido para entrar — chaves.",
            "Existe uma diferença profunda entre quem tem a chave de uma porta e quem não tem. Quem não tem, bate. Quem tem, abre. Quem tem chave não precisa esperar que alguém de dentro decida abrir — ele mesmo decide.",
            "Jesus não disse: 'Quando o céu decidir, a terra vai poder.' Ele disse: 'O que você ligar na terra terá sido ligado nos céus.' O movimento parte da terra. O céu ratifica, o céu confirma — mas a iniciativa é sua.",
            "Era para essa posição de autoridade que Adão foi criado. Ele vivia na terra com delegação plena do Criador, governando a criação como representante fiel. A cruz nos restituiu a esse lugar que Adão perdeu.",
            "Vivemos, porém, como se não tivéssemos as chaves. Batemos na porta do céu com súplicas desesperadas, como se Deus estivesse aguardando do outro lado decidindo se vai abrir. Ele já te deu as chaves — use-as.",
            "Hoje, não bata na porta do céu. Você é habitante do Reino. Você tem as chaves. Abra o que precisa ser aberto e feche o que precisa ser fechado — com a consciência de quem opera em autoridade delegada pelo próprio Rei."
        ],
        "references": ["Mateus 16:18-19", "Mateus 7:7", "Efésios 2:6", "Lucas 10:19", "Apocalipse 1:18"],
        "prayer": "Eu declaro que tenho as chaves do Reino e opero com a autoridade que Cristo me delegou — não como quem bate à porta esperando permissão, mas como quem habita o Reino e age como representante do Rei. Eu sei que o modelo mudou depois da cruz, e que agora o movimento parte de mim para o céu, que confirma e ratifica o que declaro e faço em nome de Jesus. Eu afirmo que uso essas chaves com sabedoria, com amor e com plena consciência da responsabilidade que a autoridade carrega.",
        "month_num": 1, "day_of_month": 12, "date_label": "12 de Janeiro"
    },
    {
        "day": 13, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "A Glória Compartilhada de João 17",
        "verse_text": "Eu lhes dei a glória que me deste, para que sejam um, assim como nós somos um.",
        "verse_ref": "João 17:22",
        "paragraphs": [
            "Em João 17, Jesus ora ao Pai no momento de maior tensão de Sua vida — às vésperas da cruz. E o que Ele ora? Ele não pede proteção para Si mesmo. Ele não implora para que o cálice passe. Ele intercede por você — e o que pede por você é escandaloso.",
            "Jesus declara: 'Eu lhes dei a glória que me deste.' A glória que o Pai deu ao Filho eterno, Jesus transferiu para aqueles que creem Nele. Não uma versão reduzida, não uma promessa futura — a glória. A mesma.",
            "Orar como Jesus orava não é repetir o Pai-Nosso dos discípulos que ainda não tinham cruzado o evento da ressurreição. É orar como quem conhece sua posição de unidade com o Pai e com o Filho — como quem recebeu a glória e vive dela.",
            "A oração de João 17 é uma oração de declaração, não de súplica. Jesus não pede que sejam salvos — já estão. Não pede que recebam o Espírito — vai ser enviado. Ele declara quem eles são, o que possuem e qual é a posição deles diante do Pai.",
            "João escreve em sua primeira epístola uma afirmação desconcertante: 'Como Ele é, somos nós neste mundo.' Não no céu, não na eternidade — neste mundo. Agora. Essa é a posição que a glória compartilhada nos confere.",
            "Ao fazer de João 17 seu modelo de oração, você deixa de orar como alguém que espera e começa a orar como alguém que sabe. A diferença é enorme — não apenas na postura, mas nos resultados.",
            "Ore hoje com a consciência de alguém a quem foi dada a glória do Filho. Você não é indigno diante de Deus — você é portador da glória que Deus mesmo lhe conferiu. Essa é a sua identidade."
        ],
        "references": ["João 17:1-26", "1 João 4:17", "João 14:20", "João 15:9", "Efésios 3:14-19"],
        "prayer": "Eu declaro que recebi a glória que o Pai deu ao Filho, e que vivo em unidade com o Pai e com Cristo — não como aspiração, mas como realidade presente conferida pela graça. Eu sei que minha oração não é de um indigno rogando atenção, mas de um filho falando com o Pai na intimidade da glória compartilhada. Eu afirmo que como Ele é, sou eu neste mundo — e que essa verdade define minha identidade e governa minha vida.",
        "month_num": 1, "day_of_month": 13, "date_label": "13 de Janeiro"
    },
    {
        "day": 14, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Arrependimento É Atualizar a Mente",
        "verse_text": "Arrependei-vos, porque é chegado o Reino dos céus.",
        "verse_ref": "Mateus 4:17",
        "paragraphs": [
            "A palavra grega traduzida como 'arrependimento' é metanoia — e ela não significa culpa, choro, autoagressão ou remorso. Significa literalmente mudança de mente. Meta: além. Noia: mente. Ir além da mente atual. Uma atualização radical de perspectiva.",
            "Imagine sua mente como um sistema operacional. O arrependimento bíblico não é você chorando porque o sistema está corrompido — é a instalação de uma nova versão que opera com lógicas completamente diferentes. Não é reforma — é substituição.",
            "Jesus chamou ao arrependimento porque a realidade havia mudado: 'O Reino dos céus chegou.' A mensagem era: atualize-se. Saia do sistema antigo e entre no novo. O que antes era verdade no velho sistema pode não ser mais operacional no novo.",
            "Muitos vivem com sistemas gravemente desatualizados. Pensam como se ainda estivessem no Antigo Testamento, como se a cruz não tivesse acontecido, como se o Espírito Santo não tivesse sido derramado, como se estivessem aguardando algo que já veio.",
            "O resultado é uma fé disfuncional — pessoas com o mais poderoso poder do universo dentro delas, vivendo como se fossem vítimas impotentes das circunstâncias. O sistema desatualizado interpreta mal a realidade.",
            "A renovação da mente de que Paulo fala em Romanos 12:2 é esse processo contínuo de atualização. Não é apenas ler a Bíblia — é permitir que a realidade do Reino reescreva os algoritmos com que você interpreta a vida.",
            "Hoje, identifique uma área da sua vida onde o sistema está desatualizado. Uma crença herdada da religião que não corresponde à realidade da graça. Atualize-a. Esse é o arrependimento genuíno."
        ],
        "references": ["Romanos 12:2", "Efésios 4:23", "Filipenses 4:8", "2 Coríntios 10:5", "Colossenses 3:2"],
        "prayer": "Eu declaro que minha mente está sendo continuamente atualizada pela verdade do Reino — que o arrependimento genuíno em mim não é culpa acumulada, mas transformação contínua de perspectiva que me liberta para viver na realidade plena de Cristo. Eu sei que cada vez que a verdade de Deus rompe um paradigma antigo em minha mente, estou experimentando o metanoia real que Jesus chamava. Eu afirmo que minha mente está aberta para a mais profunda atualização que o Espírito Santo quiser fazer hoje.",
        "month_num": 1, "day_of_month": 14, "date_label": "14 de Janeiro"
    },
    {
        "day": 15, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Adão Perdeu, Cristo Restituiu Tudo",
        "verse_text": "Adão foi feito alma vivente; o último Adão, porém, é espírito vivificante.",
        "verse_ref": "1 Coríntios 15:45",
        "paragraphs": [
            "Adão foi criado à imagem e semelhança de Deus — não como um ser religioso, mas como um representante com autoridade plena delegada pelo Criador para governar a Terra. Ele não era súdito, era governante. Não era servo, era filho. Essa é a posição original.",
            "A queda de Adão não foi apenas um pecado moral a ser lamentado — foi a perda de uma posição. Com o pecado, o ser humano saiu do lugar de governante e entrou no lugar de escravo; saiu da plenitude e entrou na carência; saiu da identidade de filho e entrou na ilusão de orfandade.",
            "Toda a obra da redenção pode ser resumida em uma sentença: devolver ao ser humano o que Adão perdeu. A cruz não foi apenas uma transação para limpar a culpa — foi o movimento decisivo para restaurar a posição original.",
            "Paulo revela o paralelo profundo: o primeiro Adão foi feito alma vivente — recebeu vida de Deus. O último Adão — Jesus — é espírito vivificante: Ele não apenas recebeu vida, Ele dá vida. E é essa vida que Ele nos dá ao nos unir a Si.",
            "Jesus não veio apenas nos salvar do inferno. Veio nos restituir ao jardim — à posição de filhos, herdeiros, governantes. Veio desfazer o que o primeiro Adão fez e nos reposicionar onde o Criador sempre quis que estivéssemos.",
            "Você não é um pecador salvo pela graça que ainda luta contra sua natureza pecaminosa. Você é um filho restaurado à glória original — uma nova criação que porta a natureza do último Adão, não do primeiro.",
            "Hoje, deixe para trás a identidade do primeiro Adão. Você pertence ao último — ao ressuscitado, ao vivificante, ao que restituiu o que foi perdido. Essa é a sua verdadeira identidade."
        ],
        "references": ["Gênesis 1:26-28", "Romanos 5:12-19", "1 Coríntios 15:45-49", "Efésios 1:7-10", "Colossenses 1:13-14"],
        "prayer": "Eu declaro que pertenço ao último Adão — ao Cristo ressuscitado que restituiu tudo que foi perdido no jardim — e que minha identidade não é de filho caído tentando se recuperar, mas de filho restaurado vivendo na posição original. Eu sei que a obra da redenção foi completa e que em mim foi restaurada a imagem e semelhança de Deus que o pecado havia obscurecido. Eu afirmo que vivo da natureza do último Adão, que é espírito vivificante, e que essa vida que Ele me deu governa cada área da minha existência.",
        "month_num": 1, "day_of_month": 15, "date_label": "15 de Janeiro"
    },
    {
        "day": 16, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "O Invisível É a Realidade Mais Sólida",
        "verse_text": "As coisas que se veem são temporais, e as que não se veem são eternas.",
        "verse_ref": "2 Coríntios 4:18",
        "paragraphs": [
            "Vivemos em uma cultura profundamente materialista: o que não pode ser medido, pesado ou fotografado não é considerado real. Mas Paulo afirma o exato oposto — as coisas visíveis são temporais, passageiras, transitórias. As invisíveis são eternas.",
            "Pense na ironia: a cadeira em que você senta existe há décadas. Parece permanente. Mas está se decompondo lentamente, e um dia não existirá mais. O amor de Deus por você, invisível aos sentidos físicos, nunca começou e nunca terminará.",
            "A gravidade que te mantém no chão agora mesmo é invisível — você não a vê, não a cheira, não a toca. Mas ela é mais real e mais poderosa do que a cadeira em que você senta. Assim é a realidade espiritual: invisível, mas determinante.",
            "Jesus disse a Nicodemos: 'O vento sopra onde quer, e ouves a sua voz, mas não sabes de onde vem nem para onde vai.' O vento é invisível, mas move oceanos. A realidade espiritual é invisível, mas move histórias, transforma caracteres, derruba impérios.",
            "O problema não é que Deus seja invisível — o problema é que treinamos nossos sentidos para reconhecer apenas o visível como real. Mas os que têm olhos espirituais abertos operam a partir de uma realidade que os sentidos físicos não alcançam.",
            "Paulo, escrevendo da prisão, declara que as tribulações presentes são 'leves e momentâneas' — porque ele estava fixo no invisível eterno, não no visível temporal. Essa perspectiva transforma completamente como você enfrenta as circunstâncias.",
            "Hoje, fixe seus olhos no que não se vê. As circunstâncias visíveis têm prazo de validade. A realidade invisível de Deus — Seu amor, Sua presença, Seu propósito para você — é inabalável e eterna."
        ],
        "references": ["Hebreus 11:1", "Hebreus 11:3", "João 3:8", "Romanos 8:24-25", "Colossenses 1:16"],
        "prayer": "Eu declaro que minha visão está fixada no eterno e não no temporal — que habito em uma realidade invisível que é infinitamente mais sólida e permanente do que tudo que meus olhos físicos podem ver. Eu sei que as circunstâncias visíveis ao meu redor são passageiras e sujeitas à transformação pela palavra de Deus, enquanto as realidades invisíveis do Reino são imutáveis. Eu afirmo que não me guio pelo que vejo, mas pelo que sei da realidade eterna que Deus revelou em Cristo.",
        "month_num": 1, "day_of_month": 16, "date_label": "16 de Janeiro"
    },
    {
        "day": 17, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Deus Não Cabe em Nenhuma Definição",
        "verse_text": "Grande é o Senhor e muito digno de louvor; e a sua grandeza é inescrutável.",
        "verse_ref": "Salmos 145:3",
        "paragraphs": [
            "Deus não se define. Quando disse a Moisés 'EU SOU O QUE SOU', não estava sendo evasivo — estava revelando uma verdade estrutural: o que se define se limita, e Deus é absolutamente ilimitado. Qualquer definição de Deus, por mais precisa que seja, é uma redução.",
            "Tentamos encaixar Deus em atributos: bom, justo, amoroso, poderoso. Tudo verdade. Mas Deus é infinitamente mais do que qualquer lista de atributos pode alcançar. É como descrever o oceano dizendo que é azul e molhado — correto, mas fundamentalmente insuficiente.",
            "Quando limitamos Deus às nossas definições, criamos um ídolo mental — uma versão reduzida que cabe em nossa cabeça. E passamos a adorar nossa ideia de Deus em vez de adorar o Deus real, que é grande demais para qualquer mente humana abarcar.",
            "Ele está nas profundezas dos oceanos e nas extremidades do universo. É a expressão do ar, a molécula do calor, a estrutura da matéria. É a água que sacia e o fogo que refina. É o silêncio e o trovão, a quietude e o poder.",
            "Paulo, depois de páginas elaborando a teologia mais profunda da Escritura, para subitamente em Romanos 11:33 e exclama: 'Ó profundidade da riqueza, da sabedoria e do conhecimento de Deus! Quão insondáveis são os Seus juízos e quão inexploráveis os Seus caminhos!' Até Paulo chegou no limite das palavras.",
            "Isso é libertador, não frustrante. Nossos problemas têm limites, nossas dificuldades têm fronteiras — mas nosso Deus não tem. O que parece impossível para nós é apenas mais uma ocasião para Ele demonstrar que Sua grandeza não tem borda.",
            "Quando você se aproxima de Deus em adoração hoje, deixe suas categorias de lado. Venha com abertura. Você não está revisando um conceito — está entrando na presença do ilimitado."
        ],
        "references": ["Efésios 3:20", "Isaías 55:8-9", "Romanos 11:33-36", "Jó 11:7-9", "1 Reis 8:27"],
        "prayer": "Eu declaro que meu Deus é maior que qualquer definição que já criei sobre Ele, e que a Sua grandeza inescrutável é o fundamento inabalável sobre o qual minha vida está construída. Eu sei que nenhum problema que enfrento hoje tem dimensões maiores do que o Deus ilimitado que habita em mim e que caminha comigo. Eu afirmo que adoro não minha ideia de Deus, mas o Deus real — o EU SOU O QUE SOU — cujos caminhos são inexploráveis e cuja grandeza nunca chego ao fim de descobrir.",
        "month_num": 1, "day_of_month": 17, "date_label": "17 de Janeiro"
    },
    {
        "day": 18, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Eterno, Não Apenas Infinito",
        "verse_text": "Antes que os montes nascessem, de eternidade a eternidade, Tu és Deus.",
        "verse_ref": "Salmos 90:2",
        "paragraphs": [
            "Existe uma distinção fundamental que transforma nossa compreensão de Deus: a diferença entre infinito e eterno. O infinito tem começo mas não tem fim — o universo é infinito nesse sentido. O eterno não tem começo nem fim — esse é apenas Deus.",
            "O universo é vasto para além da nossa compreensão. As galáxias se multiplicam por bilhões, as distâncias desafiam qualquer tentativa de visualização. Mas o universo teve um começo. Houve um momento em que não existia. Deus não.",
            "Antes que os montes nascessem, antes que a Terra fosse formada, antes que o espaço-tempo se desdobrasse pela primeira vez — Deus já era. Não estava em algum lugar esperando o momento de criar. Ele simplesmente era, em plena perfeição, em completa comunhão trinitária.",
            "Nosso relacionamento com Deus transcende o tempo de formas que mal conseguimos articular. Não começou quando nascemos, não terminará quando morrermos. Ele nos conhece desde a eternidade passada e já nos viu na eternidade futura.",
            "Isso confere peso eterno a cada momento presente. Cada dia que você vive, cada decisão que toma, cada ato de fé que pratica está sendo tecido em uma história que tem dimensões eternas. Nada é insignificante quando vivido diante do Eterno.",
            "Quando você passa por algo difícil — doença, perda, frustração — a perspectiva da eternidade não diminui a dor, mas a recontextualiza. O que é temporal tem limites. O Deus que está com você é eterno, e os Seus propósitos nunca se esgotam.",
            "Descanse hoje na eternidade de Deus. Ele existia antes do seu problema surgir e existirá muito depois que ele passar. Você está em mãos eternas."
        ],
        "references": ["Isaías 57:15", "2 Pedro 3:8", "Apocalipse 1:8", "Deuteronômio 33:27", "1 Timóteo 1:17"],
        "prayer": "Eu declaro que estou nas mãos do Deus eterno — sem começo e sem fim — que me conhece desde a eternidade passada e já me viu na eternidade futura, e que o Seu propósito para minha vida tem dimensões que eu ainda não posso ver. Eu sei que o que enfrento hoje é temporal, enquanto o amor de Deus por mim é eterno e seus planos para mim são imutáveis. Eu afirmo que descanso completamente na eternidade de Deus, onde minha história foi escrita antes de ser vivida.",
        "month_num": 1, "day_of_month": 18, "date_label": "18 de Janeiro"
    },
    {
        "day": 19, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "A Igreja Começa em Atos, Não em Mateus",
        "verse_text": "Recebereis poder, ao descer sobre vós o Espírito Santo, e sereis minhas testemunhas.",
        "verse_ref": "Atos 1:8",
        "paragraphs": [
            "Existe uma confusão hermenêutica profunda que afeta a grande maioria dos cristãos: tratamos os quatro evangelhos como se fossem literatura do Novo Testamento, quando na verdade são a conclusão do Antigo. A era da Igreja não começa em Mateus — começa em Atos.",
            "Mateus, Marcos, Lucas e João narram a vida de Jesus num contexto histórico-teológico que ainda é o do judaísmo. Jesus debate com fariseus, interpreta a Torah, cura no sábado para provocar discussões. A maioria de Seus ensinamentos era dirigida a um povo sob lei, não a um povo sob graça.",
            "Muitos dos ensinamentos de Jesus nos evangelhos eram anúncios proféticos do que estaria por vir, não instruções práticas para a era da Igreja. Quando aplicamos esses textos diretamente à nossa vida sem discernimento do contexto, criamos confusão teológica e frustrações espirituais.",
            "A era da Igreja começa em Atos 2, com o derramamento do Espírito Santo. É a partir dali que somos convocados a construir nossa vida cristã. Ali começa a experiência do novo nascimento, da habitação do Espírito, da autoridade delegada ao crente.",
            "Isso não diminui os evangelhos — torna-os ainda mais ricos quando lidos no contexto correto. Jesus estava preparando o caminho para Atos. Os evangelhos são o anúncio; Atos é o cumprimento. As epístolas são a explicação do que Atos inaugurou.",
            "Quando você aplica ao seu cotidiano textos específicos para contextos históricos diferentes, o resultado é confusão. Quando aplica as epístolas — escritas para a Igreja da era do Espírito — os resultados são transformadores.",
            "Leia a Bíblia com esse mapa temporal em mente. Você não está no Egito esperando o Êxodo. Você não está em Israel esperando o Messias. Você está em Atos — na era do Espírito, na plenitude do que foi prometido."
        ],
        "references": ["Atos 2:1-4", "Hebreus 8:13", "2 Coríntios 3:6", "Gálatas 3:24-25", "Hebreus 9:15"],
        "prayer": "Eu declaro que vivo na era do Espírito — inaugurada em Atos 2 e ainda em pleno vigor — e que o poder prometido por Jesus aos discípulos é o mesmo poder que opera em mim hoje pelo Espírito Santo. Eu sei que não sou herdeiro de uma religião de lei, mas cidadão de uma era de graça, onde o Espírito Santo é o Guia, o Consolador e o Poder que habita em mim. Eu afirmo que leio as Escrituras com discernimento da era em que vivo, e que aplico à minha vida as verdades que foram escritas para a minha era.",
        "month_num": 1, "day_of_month": 19, "date_label": "19 de Janeiro"
    },
    {
        "day": 20, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Tal Como Ele É — Neste Mundo, Agora",
        "verse_text": "Qual Ele é, somos nós também neste mundo.",
        "verse_ref": "1 João 4:17",
        "paragraphs": [
            "João escreve uma das declarações mais escandalosas de toda a Bíblia: 'Qual Ele é, somos nós neste mundo.' Não no céu, não na eternidade futura, não depois da morte. Neste mundo. Agora. Hoje. Esta é a identidade do crente na era do Espírito.",
            "Para a mente religiosa, isso parece presunção no limite da blasfêmia. Como podemos ser como Jesus agora, ainda vivendo neste mundo imperfeito? Mas João não está descrevendo uma aspiração — está declarando uma realidade conferida pela graça.",
            "Não significa que somos Deus. Significa que nossa posição diante do Pai é idêntica à de Jesus. Filhos igualmente amados, igualmente aceitos, igualmente justificados, com pleno acesso ao trono e à herança do Pai. Essa posição não é conquistada — é recebida.",
            "À medida que permanecemos em Deus e Seu amor se torna perfeito em nós, temos confiança plena — porque vivemos como Jesus viveu: na consciência ininterrupta da filiação, do amor do Pai e da identidade de herdeiro.",
            "João continua: 'No amor não há temor; antes, o perfeito amor lança fora o temor.' Quando você vive como Jesus vive — na segurança do amor do Pai — o medo perde completamente seu poder sobre você. Não porque as circunstâncias mudem, mas porque sua identidade não tremeu.",
            "O problema é que muitos crentes vivem com uma identidade abaixo da revelada. Vivem como orfãos quando são filhos, como mendigos quando são herdeiros, como réus quando já foram justificados.",
            "Ande hoje com a cabeça erguida. Não por orgulho humano, mas por identidade revelada. Você é como Jesus é neste mundo. Isso não é exagero carismático — é a declaração sóbria e precisa da Palavra de Deus."
        ],
        "references": ["1 João 4:17", "Gálatas 2:20", "Filipenses 1:21", "Colossenses 3:3-4", "2 Coríntios 5:21"],
        "prayer": "Eu declaro que tal como Cristo é, sou eu neste mundo — não por mérito próprio, mas por identidade conferida pela graça — e que essa realidade governa como me relaciono comigo mesmo, com os outros e com Deus. Eu sei que minha posição diante do Pai é idêntica à de Jesus: filho amado, aceito, justificado, habitante do Reino neste mundo agora mesmo. Eu afirmo que vivo dessa identidade em cada circunstância, e que o amor perfeito do Pai em mim expulsa qualquer forma de medo ou insegurança.",
        "month_num": 1, "day_of_month": 20, "date_label": "20 de Janeiro"
    },
    {
        "day": 21, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "O Vento do Espírito Sopra Onde Quer",
        "verse_text": "O Espírito sopra onde quer, e ouves a sua voz, mas não sabes de onde vem nem para onde vai.",
        "verse_ref": "João 3:8",
        "paragraphs": [
            "Quando Jesus escolheu o vento como metáfora para o Espírito Santo, estava dizendo algo profundo sobre a natureza divina: o Espírito é livre, soberano e incontrolável. Nenhuma estrutura religiosa pode domesticá-Lo. Nenhuma liturgia pode convocá-Lo ou dispensá-Lo. Ele sopra onde quer.",
            "A religião ao longo da história sempre tentou colocar o Espírito em uma caixa: liturgias, programações, formatos de culto, tradições que garantiriam a presença de Deus se seguidas corretamente. Mas o vento não pede permissão. Ele sopra, e você ouve — ou não ouve.",
            "Jesus usou essa imagem com Nicodemos para revelar que o novo nascimento não é fruto de esforço humano, não é produto de disciplina religiosa, não é resultado de acumulação de mérito. É obra soberana do Espírito que sopra onde quer.",
            "Isso não significa passividade — significa disponibilidade. O marinheiro não cria o vento, mas posiciona as velas para que o vento o leve onde precisa ir. Assim é a vida no Espírito: não tentamos controlar, mas nos posicionamos para ser levados.",
            "Muitas igrejas ficaram sem vento porque tentaram controlar o que só pode ser recebido. Organizaram o mover do Espírito em horários e formatos. E um dia perceberam que estavam fazendo muitas coisas, mas com Sua ausência.",
            "A vida autêntica no Espírito é uma aventura constante de não saber de onde Ele vem ou para onde vai — mas confiar plenamente que onde Ele leva é exatamente onde você precisa estar.",
            "Abra-se hoje para o sopro imprevisível e soberano do Espírito. Solte o controle. Posicione suas velas. E deixe-O levar você para lugares que sua mente jamais planejaria."
        ],
        "references": ["Atos 2:2-4", "João 14:26", "João 16:13", "Romanos 8:14", "Gálatas 5:25"],
        "prayer": "Eu declaro que sou movido pelo Espírito Santo — que como o vento que sopra onde quer, Ele governa meus passos, abre meus caminhos e me leva onde o Pai quer me ter, mesmo que minha mente não consiga mapear a rota. Eu sei que tentar controlar o Espírito é perder o Espírito, e que a rendição soberana a Ele é o único caminho para a vida plena que Jesus prometeu. Eu afirmo que hoje tenho minhas velas posicionadas e estou disponível para o sopro imprevisível e transformador do Espírito de Deus.",
        "month_num": 1, "day_of_month": 21, "date_label": "21 de Janeiro"
    },
    {
        "day": 22, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "D'Ele, Por Ele e Para Ele São Todas as Coisas",
        "verse_text": "Porque d'Ele, por Ele e para Ele são todas as coisas. A Ele seja a glória eternamente.",
        "verse_ref": "Romanos 11:36",
        "paragraphs": [
            "Depois de onze capítulos da teologia mais profunda já escrita, Paulo chega a uma conclusão que transcende qualquer argumento: 'D'Ele, por Ele e para Ele são todas as coisas.' Deus é a fonte, o meio e o destino de toda a realidade existente.",
            "D'Ele — tudo veio de Deus. Nenhuma partícula de matéria, nenhuma lei física, nenhum momento no tempo existiu sem que Deus fosse o ponto de origem. Não há nada no universo que não seja criação de Deus, expressão de Deus, revelação de Deus.",
            "Por Ele — tudo subsiste por Deus. Colossenses 1:17 diz que em Cristo 'todas as coisas subsistem'. Se Deus retirasse Sua sustentação da realidade por um instante, tudo simplesmente deixaria de existir. Você está sendo sustentado ativamente pelo poder de Deus agora mesmo.",
            "Para Ele — tudo existe com destino em Deus. Não há história sem fim, não há criação sem propósito, não há vida sem destino. Tudo que existe está se movendo em direção ao momento em que Deus será tudo em todos.",
            "Isso significa que nada está fora do alcance de Deus. Não existe problema que não começou n'Ele e que não pode ser resolvido por Ele. Não existe dor que esteja além de Seu cuidado, não existe confusão que esteja fora de Sua soberania.",
            "A ciência mapeia as leis do universo com beleza crescente. Mas não consegue responder por que essas leis existem. A resposta da fé é: porque Deus É, e o universo inteiro é o palco onde Ele se revela e onde Seus filhos vivem.",
            "Você não está perdido em um universo indiferente. Está dentro de um universo que d'Ele veio, por Ele existe e para Ele vai. Você é parte de uma história que tem autor, tem propósito e tem um fim glorioso."
        ],
        "references": ["Atos 17:28", "Colossenses 1:17", "Hebreus 1:3", "João 1:3", "Neemias 9:6"],
        "prayer": "Eu declaro que minha vida existe dentro do fluxo eterno que vem de Deus, passa por Ele e retorna a Ele — e que cada circunstância da minha história está dentro dessa soberania absoluta que garante que nada é acidente e nada é sem propósito. Eu sei que estou sendo sustentado ativamente pelo poder de Deus neste exato momento, e que o mesmo poder que sustenta o universo está operando a meu favor. Eu afirmo que minha história tem destino em Deus — e que esse destino é glorioso.",
        "month_num": 1, "day_of_month": 22, "date_label": "22 de Janeiro"
    },
    {
        "day": 23, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Você É o Templo Vivo de Deus",
        "verse_text": "Não sabeis que sois santuário de Deus e que o Espírito de Deus habita em vós?",
        "verse_ref": "1 Coríntios 3:16",
        "paragraphs": [
            "Durante séculos, o templo de Deus foi um edifício — primeiro o tabernáculo no deserto, depois o templo de Salomão em Jerusalém. A presença de Deus habitava no Santo dos Santos, acessível apenas ao sumo sacerdote, uma vez por ano, com sangue de animais.",
            "Então o Espírito Santo foi derramado em Atos 2, e tudo mudou. Paulo faz a pergunta que deveria revolucionar toda a teologia cristã: 'Não sabeis que sois santuário de Deus?' Não a igreja onde você frequenta. Você.",
            "O Espírito de Deus não habita mais em edifícios feitos por mãos humanas. Ele habita em templos vivos — em você. A mais extraordinária das migrações: da pedra para a carne, do estático para o dinâmico, do geográfico para o pessoal.",
            "Isso muda completamente sua vida de oração. Você não precisa ir a um lugar sagrado para encontrar Deus — você já é o lugar sagrado. Não precisa criar as condi��ões certas para que Deus apareça — Ele já está aqui, em você.",
            "Significa também que onde quer que você vá, o templo de Deus vai junto. No trabalho, no mercado, na escola, na rua. Toda vez que você entra em um lugar, a presença de Deus entra com você. Você é portador da shekinah.",
            "Paulo usa a palavra 'santuário' — não apenas habitação. O santuário é o lugar santificado, separado, dedicado à glória de Deus. Você foi santificado, separado e dedicado para ser morada de Deus na Terra.",
            "Cuide do templo. Não apenas fisicamente — espiritualmente, emocionalmente, mentalmente. Você não é apenas um recipiente de carne — é a morada escolhida pelo Deus do universo para habitar na Terra."
        ],
        "references": ["1 Coríntios 6:19", "2 Coríntios 6:16", "João 14:23", "Efésios 2:21-22", "Colossenses 1:27"],
        "prayer": "Eu declaro que sou templo vivo do Deus do universo — que o Espírito Santo habita em mim como Sua morada escolhida — e que essa realidade transforma como me vejo, como me trato e como me movo pelo mundo. Eu sei que não vou ao encontro de Deus em lugares geográficos porque Ele já está em mim, e que onde eu for, a presença de Deus vai comigo. Eu afirmo que trato meu templo com honra, porque a habitação do Altíssimo merece o maior cuidado.",
        "month_num": 1, "day_of_month": 23, "date_label": "23 de Janeiro"
    },
    {
        "day": 24, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "O Verbo Se Fez Carne — O Maior Mistério",
        "verse_text": "E o Verbo se fez carne e habitou entre nós, e vimos a sua glória.",
        "verse_ref": "João 1:14",
        "paragraphs": [
            "O maior evento da história universal não foi a fundação de um império, a descoberta de um continente ou a chegada à lua. Foi este: o Verbo eterno — através do qual todas as coisas foram feitas — se fez carne. O eterno entrou no temporal. O infinito se fez finito. O Criador se tornou criatura.",
            "A encarnação não é uma diminuição de Deus mas uma revelação completa de Seu amor. Deus poderia ter resgatado a humanidade de muitas formas. Mas escolheu a mais íntima: vir pessoalmente. Não enviou um representante, um anjo, uma mensagem — Ele veio.",
            "Jesus sentiu fome. Ficou cansado depois de jornadas longas. Chorou diante do túmulo de Lázaro — não por não saber que iria ressuscitá-lo, mas porque amava genuinamente. Ele não fingiu ser humano — foi plenamente humano, sem deixar de ser plenamente Deus.",
            "Isso tem uma implicação profunda para o sofrimento humano: não existe experiência humana que Deus não compreenda de dentro. Quando você sofre, o Deus que se fez carne não te observa de longe com distância divina — Ele conhece a dor por experiência própria.",
            "A encarnação prova que Deus não apenas nos ama — Ele nos valoriza o suficiente para se tornar um de nós. Nenhuma religião jamais ousou fazer essa afirmação. Nenhum outro deus na história foi tão longe no alcance do amor.",
            "E o mais extraordinário: a encarnação continua. João diz que o Verbo 'habitou entre nós' — a palavra grega é eskēnōsen, literalmente 'armou Sua tenda entre nós'. Agora Ele arma Sua tenda em você. A encarnação prossegue no Corpo de Cristo.",
            "Você não crê em um Deus distante e frio. Crê no Verbo que se fez carne, que sabe o que é ser humano, e que escolheu continuar habitando entre os humanos — em você, pelo Espírito."
        ],
        "references": ["Filipenses 2:6-8", "Hebreus 2:14-17", "1 Timóteo 3:16", "João 1:1-3", "Colossenses 2:9"],
        "prayer": "Eu declaro que o Deus que se fez carne não é distante nem indiferente ao meu sofrimento — Ele conhece a experiência humana de dentro, e Seu amor por mim foi tão extravagante que o levou a deixar a glória do céu para se tornar um de nós. Eu sei que a encarnação continua em mim pelo Espírito, e que sou chamado a ser a expressão do Verbo encarnado no mundo ao meu redor. Eu afirmo que o mistério da encarnação não é apenas história — é a minha identidade: portador do Deus que se fez carne.",
        "month_num": 1, "day_of_month": 24, "date_label": "24 de Janeiro"
    },
    {
        "day": 25, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Jesus Cristo — Ontem, Hoje e Eternamente o Mesmo",
        "verse_text": "Jesus Cristo é o mesmo ontem, hoje e eternamente.",
        "verse_ref": "Hebreus 13:8",
        "paragraphs": [
            "Uma frase de oito palavras que contém uma das verdades mais revolucionárias para a vida prática da fé: Jesus Cristo é o mesmo ontem, hoje e eternamente. Não um Jesus histórico que viveu há dois mil anos. O mesmo Jesus. Vivo, presente, imutável, aqui.",
            "O Jesus que caminhou sobre as águas do mar da Galileia é o mesmo que caminha com você hoje. O Jesus que curou leprosos com um toque é o mesmo que pode tocar o que em você ainda está enfermo. O Jesus que ressuscitou Lázaro é o mesmo que fala ressurreição nas situações mortas da sua vida.",
            "Isso significa que o poder que você lê nos evangelhos não é um poder histórico arquivado. É um poder presente. A mesma unção que operava em Jesus opera no Seu corpo — que é você — pelo Espírito Santo. O que Ele fez ontem, pode e quer fazer hoje.",
            "Muitos tratam Jesus como um personagem admirável de um livro antigo — alguém cujos ensinamentos são valiosos, cujo exemplo é inspirador, mas cuja ação direta na vida presente é incerta ou rara. Isso é tratar o imutável como se fosse limitado pelo tempo.",
            "Jesus não mudou. Sua compaixão não arrefeceu, Seu poder não diminuiu, Seu amor não esfriou, Sua disposição de intervir na história humana não se reduziu. O que mudou foi nossa capacidade de esperar por Sua intervenção.",
            "A imutabilidade de Jesus é sua âncora em um mundo de mudanças constantes. Quando tudo ao redor parece incerto, Ele permanece o mesmo. Quando você muda — para melhor ou para pior — Ele permanece o mesmo.",
            "Ore hoje com a confiança de que fala com o Jesus vivo — o mesmo da Galileia, o mesmo do Gólgota, o mesmo do túmulo vazio. Não com uma memória. Com uma Pessoa presente."
        ],
        "references": ["Hebreus 13:8", "Mateus 28:20", "Apocalipse 1:17-18", "João 14:12", "Atos 1:1"],
        "prayer": "Eu declaro que sirvo ao Jesus vivo e imutável — o mesmo ontem, hoje e eternamente — e que o poder que operava nEle quando andava na Galileia é o mesmo poder que opera em mim pelo Espírito Santo hoje. Eu sei que a imutabilidade de Jesus é minha âncora — que quando tudo muda ao meu redor, Ele permanece o mesmo, e isso é suficiente para que eu não trema. Eu afirmo que espero o mesmo Jesus que o livro de Atos registrou — pleno de poder, compassivo, soberano — operando na minha vida neste dia.",
        "month_num": 1, "day_of_month": 25, "date_label": "25 de Janeiro"
    },
    {
        "day": 26, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "A Plenitude dos Tempos Chegou Para Você",
        "verse_text": "Havendo Deus falado muitas vezes aos pais pelos profetas, nestes últimos dias nos falou pelo Filho.",
        "verse_ref": "Hebreus 1:1-2",
        "paragraphs": [
            "Hebreus abre com uma declaração de contraste extraordinário: antes, Deus falou de muitas formas e em muitos fragmentos pelos profetas. Agora, nos últimos dias, Ele falou pelo Filho — e não há mais nada a ser dito. Jesus é a Palavra final e definitiva de Deus à humanidade.",
            "Os profetas foram mensageiros fiéis. Cada um carregou um fragmento da revelação divina, como peças de um quebra-cabeça. Isaías viu o servo sofredor. Daniel viu o Filho do homem. Jeremias anunciou a nova aliança. Mas nenhum deles viu o quadro completo.",
            "Você vive com o quadro completo em mãos. Cristo veio, revelou, morreu, ressuscitou, enviou o Espírito. Não há revelação pendente, não há etapa faltante, não há promessa sem cumprimento. A plenitude chegou.",
            "Isso nos torna as pessoas mais privilegiadas de toda a história humana. Reis e profetas desejaram ver o que você vê e não viram. João Batista — a quem Jesus chamou de o maior dos profetas — anunciou a chegada de Quem você já conhece pessoalmente.",
            "O problema não é falta de revelação — é excesso de inconsciência. Temos mais acesso à presença e ao conhecimento de Deus do que qualquer geração anterior, mas vivemos muitas vezes como se estivéssemos no começo da história.",
            "Desperte para o privilégio de sua era. Você nasceu no momento certo, no lado certo da revelação, com acesso ao que toda a criação aguardou por milênios. Não subestime o que foi dado a você.",
            "Viva hoje à altura de quem você é: um ser humano que nasceu na plenitude dos tempos, com o Espírito de Deus habitando em si e todas as riquezas de Cristo disponíveis a qualquer momento."
        ],
        "references": ["Gálatas 4:4-5", "Efésios 1:10", "1 Pedro 1:10-12", "Mateus 13:17", "Lucas 10:24"],
        "prayer": "Eu declaro que nasci na plenitude dos tempos — com acesso ao que profetas e reis desejaram ver e não viram — e que o privilégio desta era é minha responsabilidade de viver plenamente. Eu sei que em Cristo todas as riquezas da sabedoria e do conhecimento estão escondidas, e que tenho acesso total a essas riquezas por habitação do Espírito Santo. Eu afirmo que vivo à altura do privilégio desta era — como filho da plenitude, não como órfão de promessas ainda por vir.",
        "month_num": 1, "day_of_month": 26, "date_label": "26 de Janeiro"
    },
    {
        "day": 27, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Você É a Coroa — Não o Acidente — da Criação",
        "verse_text": "Fizeste-o um pouco menor do que os anjos, de glória e de honra o coroaste.",
        "verse_ref": "Salmos 8:5",
        "paragraphs": [
            "Davi contempla o céu estrelado e fica impressionado não com a vastidão do universo — mas com o fato de que Deus, diante de tudo isso, se importa com o ser humano. 'Que é o homem, para que d'Ele Te lembres?' E então responde sua própria pergunta: é a coroa da criação, coroado de glória e honra.",
            "A cultura contemporânea tende a diminuir o ser humano diante da vastidão do cosmos — somos apenas poeira cósmica em um planeta médio de uma galáxia entre bilhões. Mas isso é a perspectiva do telescópio, não a perspectiva do Criador.",
            "Deus não criou o universo e depois encaixou o ser humano onde coube. Criou o ser humano como propósito central e construiu o universo como o ambiente perfeito para que esse filho amado florescesse. Você não é acidente do cosmos — é o destinatário do cosmos.",
            "A religião ao longo da história frequentemente nos ensinou que somos vermes diante de Deus — miseráveis, indignos, radicalmente corrompidos. Mas Davi diz que fomos coroados de glória e honra. Os dois não podem ser verdade ao mesmo tempo.",
            "A humildade bíblica não é me diminuir — é reconhecer o que Deus fez de mim e viver à altura disso com gratidão, não com orgulho. É honrar o Criador honorando Sua obra-prima. Negar que você foi coroado de glória não é humildade — é ingratidão.",
            "Você é portador da imagem de Deus — imago Dei. Não uma cópia fraca ou uma réplica defeituosa. A imagem genuína do Criador, impressa em ser de carne e espírito, destinada a refletir Sua glória na Terra.",
            "Viva com consciência dessa coroa. Com responsabilidade pelo mundo a seu cuidado, com compaixão pelos outros portadores da imagem, com gratidão ao Criador por tudo que faz você ser exatamente quem é."
        ],
        "references": ["Gênesis 1:26-28", "Salmos 8:3-8", "Gênesis 2:15", "Tiago 1:18", "Salmos 139:14"],
        "prayer": "Eu declaro que sou portador da imagem de Deus — coroado de glória e honra pelo próprio Criador — e que viver abaixo dessa identidade não é humildade, mas ingratidão diante de Quem me fez. Eu sei que fui criado como propósito central da criação, e que cada detalhe deste mundo foi preparado para que eu florescesse e refletisse a glória do Pai. Eu afirmo que caminho com a coroa que Deus me colocou — não por orgulho humano, mas por fidelidade à identidade que o Criador me conferiu.",
        "month_num": 1, "day_of_month": 27, "date_label": "27 de Janeiro"
    },
    {
        "day": 28, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Conte Seus Dias Com Sabedoria Eterna",
        "verse_text": "Ensina-nos a contar os nossos dias, para que alcancemos coração sábio.",
        "verse_ref": "Salmos 90:12",
        "paragraphs": [
            "Moisés — que escreveu o Salmo 90 — faz um pedido aparentemente simples: 'Ensina-nos a contar os nossos dias.' Mas o que significa contar os dias? Não é organizar uma agenda ou marcar datas no calendário. É uma operação espiritual de perspectiva transformadora.",
            "Contar os dias é somar à sua existência toda a história de Deus que precede o seu nascimento. Quando você conta seus dias dessa maneira, percebe que não tem apenas os anos que viveu — você tem milênios de história de Deus somados à sua vida.",
            "A criação — que aconteceu antes de você — é parte dos seus dias. A vinda de Cristo — que aconteceu antes de você — é parte dos seus dias. Todos os atos de Deus registrados nas Escrituras, todos os milagres, todas as promessas cumpridas — são parte da sua história.",
            "Um coração sábio é aquele que vive com essa perspectiva ampliada. Que não se deixa escravizar pelo presente imediato porque enxerga o passado profundo e o futuro glorioso. Que não tremeu diante das circunstâncias de hoje porque sabe Quem estava presente em todas as circunstâncias da história.",
            "Paulo escreve com urgência em Efésios: 'Aproveitai o tempo.' A palavra grega é exagorazō — literalmente 'compre de volta o tempo', resgate o tempo. Cada dia tem um valor que precisa ser reconhecido e honrado.",
            "Quando você conta seus dias com sabedoria — somando a história de Deus à sua história — percebe que sua existência é mais rica, mais significativa e mais conectada do que imaginava. Você não é um indivíduo isolado — é parte de uma história que começou na eternidade.",
            "Hoje, conte seus dias. Some à sua vida o Deus que criou o mundo para você, que veio em Cristo para te resgatar, que enviou o Espírito para habitar em você. Que coração sábio isso produz."
        ],
        "references": ["Salmos 90:12", "Efésios 5:15-16", "Colossenses 4:5", "Tiago 4:14", "Salmos 39:4"],
        "prayer": "Eu declaro que conto meus dias com sabedoria eterna — somando à minha existência toda a história de Deus que me precedeu — e que essa perspectiva ampliada me liberta da tirania do presente imediato. Eu sei que não tenho apenas os anos de minha vida breve, mas milênios de fidelidade de Deus como herança e fundamento. Eu afirmo que vivo cada dia com consciência do seu valor eterno, resgatando o tempo e fazendo de cada momento um depósito na conta do propósito de Deus para minha vida.",
        "month_num": 1, "day_of_month": 28, "date_label": "28 de Janeiro"
    },
    {
        "day": 29, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "O Deus Que Se Revela — Sem Parar",
        "verse_text": "As coisas encobertas pertencem ao Senhor, mas as reveladas nos pertencem.",
        "verse_ref": "Deuteronômio 29:29",
        "paragraphs": [
            "Há um equívoco frequente na espiritualidade cristã: a ideia de que Deus se esconde e nós precisamos encontrá-Lo através de disciplinas suficientes. Mas a Bíblia revela o oposto: Deus é um Deus que se revela. Revelar é a Sua natureza. Ele quer ser conhecido.",
            "Existem coisas encobertas que pertencem à soberania de Deus — mistérios que Ele, em Sua sabedoria, reserva para Si. Não é nossa função investigar o que Ele optou por não revelar. Mas as coisas que Ele revelou nos pertencem — e são muitas, suficientes para viver em plenitude.",
            "Deus se revela na criação: 'Os céus declaram a glória de Deus.' Cada nascer do sol é uma revelação. Cada flor que abre, cada onda que quebra na praia, cada sorriso de criança — tudo é Deus se mostrando.",
            "Deus se revela nas Escrituras com clareza e profundidade crescentes. Cada leitura que você faz das mesmas páginas pode trazer uma revelação nova — porque o Espírito Santo nunca esgota o que tem a mostrar.",
            "Deus se revela pelo Espírito que habita em você. Paulo ora em Efésios que Deus nos dê 'espírito de sabedoria e de revelação no pleno conhecimento d'Ele.' A revelação não é para os excepcionais — é promessa para todo crente.",
            "O problema não é falta de revelação. É que muitos buscam experiências místicas espetaculares enquanto ignoram a revelação silenciosa e constante que Deus oferece em cada detalhe do dia. Ele está sempre se mostrando. Você está sempre olhando?",
            "Hoje, abra seus olhos para a revelação ordinária de Deus. Na Escritura que você vai ler, na conversa que vai ter, na beleza que vai cruzar seu caminho. Ele está se revelando — sem parar."
        ],
        "references": ["Romanos 1:19-20", "Mateus 11:25", "1 Coríntios 2:10", "Efésios 1:17-18", "Daniel 2:22"],
        "prayer": "Eu declaro que o Deus que sirvo é o Deus que se revela — que Sua natureza não é se esconder, mas se mostrar — e que tenho olhos espirituais abertos para perceber Sua revelação constante em cada detalhe da criação, das Escrituras e da minha vida diária. Eu sei que não busco a Deus como quem procura algo perdido, mas como quem abre os olhos para o que sempre esteve presente. Eu afirmo que vivo com receptividade plena à revelação do Espírito Santo, que ilumina para mim mais de Cristo a cada dia.",
        "month_num": 1, "day_of_month": 29, "date_label": "29 de Janeiro"
    },
    {
        "day": 30, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "A Verdade Que Liberta — Não Que Aprisiona",
        "verse_text": "E conhecereis a verdade, e a verdade vos libertará.",
        "verse_ref": "João 8:32",
        "paragraphs": [
            "Jesus fez uma promessa extraordinária e paradoxal para o pensamento religioso: a verdade liberta. Não aprisiona, não condena, não esmaga — liberta. Se o que você chama de verdade produz aprisionamento em culpa, medo e condenação, não é a verdade de Cristo. É outra coisa.",
            "A religião ao longo da história frequentemente usou a verdade como arma de controle. 'A verdade é que você é pecador.' 'A verdade é que você não merece.' 'A verdade é que Deus vai julgá-lo.' Isso produz escravidão religiosa, não libertação espiritual.",
            "A verdade que Jesus anuncia é esta: você é amado, aceito, justificado, habitado pelo Espírito, coroado de glória, escolhido antes da fundação do mundo, herdeiro de todas as promessas. Isso — isso sim — liberta.",
            "Jesus diz 'conhecereis a verdade' — e a palavra grega é ginōskō: conhecimento experiencial, íntimo, transformador. Não é apenas saber intelectualmente. É uma revelação que entra no ser e transforma de dentro para fora.",
            "Muitas pessoas conhecem a Bíblia de memória mas não foram libertadas. Porque memorizaram informações mas não tiveram revelação. A diferença é enorme: informação enche a cabeça, revelação transforma o coração e muda a vida.",
            "Que área da sua vida ainda está em cativeiro? Que crença antiga ainda te aprisiona? Leve isso ao Espírito Santo com honestidade e peça: 'Mostra-me a verdade que liberta nessa área.' Ele sempre responde a essa oração.",
            "A verdade de Cristo não pesa — ela descarrega. Não condena — ela reconcilia. Não aprisiona — ela abre as portas do calabouço e diz: você é livre. Porque o Filho te libertou, és verdadeiramente livre."
        ],
        "references": ["João 8:32", "João 14:6", "João 17:17", "2 Timóteo 2:15", "João 16:13"],
        "prayer": "Eu declaro que a verdade de Cristo opera em mim como libertação — não como aprisionamento — e que cada revelação do Espírito Santo em minha vida abre uma porta que a religião havia fechado. Eu sei que ser verdadeiramente livre é o propósito para o qual Cristo me libertou, e que nenhuma forma de escravidão — ao pecado, à culpa, ao medo, à religião — tem poder sobre quem conhece a verdade que liberta. Eu afirmo que sou livre — não por meu próprio esforço, mas porque o Filho me libertou, e a liberdade que o Filho dá é verdadeira e completa.",
        "month_num": 1, "day_of_month": 30, "date_label": "30 de Janeiro"
    },
    {
        "day": 31, "month": "Janeiro", "theme": "A Natureza de Deus",
        "title": "Escolhido Antes — Destinado Para Sempre",
        "verse_text": "Nos escolheu n'Ele antes da fundação do mundo, para sermos santos e irrepreensíveis perante Ele.",
        "verse_ref": "Efésios 1:4",
        "paragraphs": [
            "Paulo escreve as palavras mais vertiginosas sobre identidade que o Novo Testamento contém: antes da fundação do mundo, Deus nos escolheu em Cristo. Não depois do nosso nascimento, não depois da nossa conversão, não depois de provarmos algo — antes. Antes de tudo.",
            "Você não foi escolhido porque Deus previu que você seria suficientemente bom. Foi escolhido porque Deus é suficientemente amoroso. A eleição divina não está baseada no mérito humano — está baseada no caráter de Deus. E o caráter de Deus não muda.",
            "'Para sermos santos e irrepreensíveis perante Ele' — não como condição de permanência, mas como propósito da escolha. Deus não te escolheu para que você se tornasse digno da escolha. Te escolheu para que a santidade florescesse em você como fruto da eleição.",
            "Essa verdade destrói toda a insegurança existencial que a religião produziu ao longo dos séculos. Você não está em probação, esperando saber se vai ser mantido ou descartado. A escolha foi feita antes da fundação do mundo, e o Deus que escolheu é eterno — Sua escolha também é.",
            "Antes de existir espaço, você estava no coração de Deus. Antes de existir tempo, o Pai tinha um propósito para você. Antes de qualquer decisão sua — boa ou ruim — Deus disse: 'Esse é meu.'",
            "Ao encerrar Janeiro, o mês em que mergulhamos na natureza de Deus, deixe que essa verdade fique gravada no mais profundo do seu ser: você não está descobrindo se é amado — você é amado desde antes de existir. Não está construindo uma relação com Deus — está vivendo dentro de uma relação que começou na eternidade.",
            "Descanse nessa escolha. Não como doutrina para debates teológicos, mas como rocha sob os seus pés em todo e qualquer dia de tempestade. Você foi escolhido. Antes da fundação do mundo. Pelo Deus que não muda."
        ],
        "references": ["Efésios 1:4-5", "2 Tessalonicenses 2:13", "1 Pedro 1:2", "Romanos 8:29-30", "2 Timóteo 1:9"],
        "prayer": "Eu declaro que fui escolhido em Cristo antes da fundação do mundo — não por mérito meu, mas por amor eterno de Deus — e que essa escolha é imutável como é imutável o caráter do Deus que a fez. Eu sei que a minha identidade não flutua com minhas performances nem com as opiniões alheias, porque está fundamentada em uma escolha feita na eternidade pelo próprio Criador. Eu afirmo que carrego com gratidão e responsabilidade o peso glorioso de ser o escolhido do Eterno — e que essa verdade governa cada dia dos 365 que me foram dados nesta jornada.",
        "month_num": 1, "day_of_month": 31, "date_label": "31 de Janeiro"
    }
]

# Read original file
src = '/home/dev/workspace/devocional-escandalo-da-graca/devocional365/js/devotionals.js'
with open(src, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.index('[')
end = content.rindex(']') + 1
header = content[:start]
footer = content[end:]

data = json.loads(content[start:end])
non_jan = [d for d in data if d.get('month') != 'Janeiro']
new_data = JANUARY_NEW + non_jan

assert len(new_data) == 365, f'Expected 365, got {len(new_data)}'

output = header + json.dumps(new_data, ensure_ascii=False, separators=(',', ':')) + footer
with open(src, 'w', encoding='utf-8') as f:
    f.write(output)

print(f'Done! {len(new_data)} devotionals written.')
for d in JANUARY_NEW:
    words = sum(len(p.split()) for p in d['paragraphs'])
    print(f'  Day {d["day_of_month"]:02d}: {len(d["paragraphs"])} paragraphs, {words} words')

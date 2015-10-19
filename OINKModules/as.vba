    Dim WriterID As String
    Dim WriterEmail As String
    Dim WriterName As String
    Dim BU As String
    Dim SuperCategory As String
    Dim Category As String
    Dim SubCategory As String
    Dim Vertical As String
    Dim Brand As String
    Dim EditorID As String
    Dim EditorEmail As String
    Dim EditorID As String
    Dim AuditDate As Date
    Dim WeekNum As String
    Dim MonthNum As String
    Dim WSName As String
    Dim WordCount As Integer
    Dim FSN As String
    Dim Introduction As String
    Dim ProdTheme As String
    Dim ArticleFlow As String
    Dim ExplainFeatures As String
    Dim PracticalApplications As String
    Dim NeutralContent As String
    Dim USP As String
    Dim PriorityOfFeatures As String
    Dim SentenceConstruction As String
    Dim SubVerbAgreement As String
    Dim MissingAdditionalRepeatedWords As String
    Dim SpellingTypo As String
    Dim Punctuation As String
    Dim FormattingError As String
    Dim KeywordVar As String
    Dim KeywordDensity As String
    Dim Plagiarism As String
    Dim SpecMismatch As String
    Dim CFMQualityScore As Double
    Dim GSEOQualityScore As Double
    Dim CombinedQualityScore As Double
    Dim Fatals As Integer
    Dim NonFatals As Integer
    Dim Lastrow As Object
    Dim CountRows As Integer
    Dim WorkingCell As Range
    Application.ScreenUpdating = False
    
' Assign meaningful names to the variables.
' This is where you control the assignment of values.
    
    WriterName = ActiveWorkbook.Sheets("AuditSheet").Range("$E$3")
    Category = ActiveWorkbook.Sheets("AuditSheet").Range("$E$5")
    SubCategory = ActiveWorkbook.Sheets("AuditSheet").Range("$E$7")
    WeekNum = ActiveWorkbook.Sheets("AuditSheet").Range("$E$9")
    MonthName = ActiveWorkbook.Sheets("AuditSheet").Range("$E$11")
    QualityAnalyst = ActiveWorkbook.Sheets("AuditSheet").Range("$H$3")
    WSName = ActiveWorkbook.Sheets("AuditSheet").Range("$H$5")
    WordCount = ActiveWorkbook.Sheets("AuditSheet").Range("$H$7")
    FSN = ActiveWorkbook.Sheets("AuditSheet").Range("$H$9")
    AuditDate = ActiveWorkbook.Sheets("AuditSheet").Range("$H$11")
    CFMQualityScore = ActiveWorkbook.Sheets("AuditSheet").Range("$J$3")
    GSEOQualityScore = ActiveWorkbook.Sheets("AuditSheet").Range("$K$3")
    CombinedQualityScore = ActiveWorkbook.Sheets("AuditSheet").Range("$L$3")
    Introduction = ActiveWorkbook.Sheets("AuditSheet").Range("$K$17")
    ProdTheme = ActiveWorkbook.Sheets("AuditSheet").Range("$K$18")
    ArticleFlow = ActiveWorkbook.Sheets("AuditSheet").Range("$K$19")
    ExplainFeatures = ActiveWorkbook.Sheets("AuditSheet").Range("$K$20")
    PracticalApplications = ActiveWorkbook.Sheets("AuditSheet").Range("$K$21")
    NeutralContent = ActiveWorkbook.Sheets("AuditSheet").Range("$K$22")
    USP = ActiveWorkbook.Sheets("AuditSheet").Range("$K$23")
    PriorityOfFeatures = ActiveWorkbook.Sheets("AuditSheet").Range("$K$24")
    SentenceConstruction = ActiveWorkbook.Sheets("AuditSheet").Range("$K$26")
    SubVerbAgreement = ActiveWorkbook.Sheets("AuditSheet").Range("$K$27")
    MissingAdditionalRepeatedWords = ActiveWorkbook.Sheets("AuditSheet").Range("$K$28")
    SpellingTypo = ActiveWorkbook.Sheets("AuditSheet").Range("$K$29")
    Punctuation = ActiveWorkbook.Sheets("AuditSheet").Range("$K$30")
    FormattingError = ActiveWorkbook.Sheets("AuditSheet").Range("$K$31")
    KeywordVar = ActiveWorkbook.Sheets("AuditSheet").Range("$K$33")
    KeywordDensity = ActiveWorkbook.Sheets("AuditSheet").Range("$K$35")
    Plagiarism = ActiveWorkbook.Sheets("AuditSheet").Range("$K$36")
    SpecMismatch = ActiveWorkbook.Sheets("AuditSheet").Range("$K$37")
    Fatals = ActiveWorkbook.Sheets("AuditSheet").Range("$K$9")
    NonFatals = ActiveWorkbook.Sheets("AuditSheet").Range("$K$11")
    commentIntroduction = ActiveWorkbook.Sheets("AuditSheet").Range("$L$17")
    commentProdTheme = ActiveWorkbook.Sheets("AuditSheet").Range("$L$18")
    commentArticleFlow = ActiveWorkbook.Sheets("AuditSheet").Range("$L$19")
    commentExplainFeatures = ActiveWorkbook.Sheets("AuditSheet").Range("$L$20")
    commentPracticalApplications = ActiveWorkbook.Sheets("AuditSheet").Range("$L$21")
    commentNeutralContent = ActiveWorkbook.Sheets("AuditSheet").Range("$L$22")
    commentUSP = ActiveWorkbook.Sheets("AuditSheet").Range("$L$23")
    commentPriorityOfFeatures = ActiveWorkbook.Sheets("AuditSheet").Range("$L$24")
    commentSentenceConstruction = ActiveWorkbook.Sheets("AuditSheet").Range("$L$26")
    commentSubVerbAgreement = ActiveWorkbook.Sheets("AuditSheet").Range("$L$27")
    commentMissingAdditionalRepeatedWords = ActiveWorkbook.Sheets("AuditSheet").Range("$L$28")
    commentSpellingTypo = ActiveWorkbook.Sheets("AuditSheet").Range("$L$29")
    commentPunctuation = ActiveWorkbook.Sheets("AuditSheet").Range("$L$30")
    commentFormattingError = ActiveWorkbook.Sheets("AuditSheet").Range("$L$31")
    commentKeywordVar = ActiveWorkbook.Sheets("AuditSheet").Range("$L$33")
    commentKeywordDensity = ActiveWorkbook.Sheets("AuditSheet").Range("$L$35")
    commentPlagiarism = ActiveWorkbook.Sheets("AuditSheet").Range("$L$36")
    commentSpecMismatch = ActiveWorkbook.Sheets("AuditSheet").Range("$L$37")
    

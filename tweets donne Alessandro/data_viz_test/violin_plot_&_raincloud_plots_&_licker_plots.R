# http://www.sthda.com/english/wiki/ggplot2-violin-plot-quick-start-guide-r-software-and-data-visualization
# https://www.tutorialspoint.com/how-to-set-the-y-axis-tick-marks-using-ggplot2-in-r

rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/ULTIMA_VERSIONE/Questionario Psicometrico_PRIME_RISPOSTE/1.VIZ")

library(readxl)
library(ggplot2)



db_violin <- read_excel("v_plot_TEST.xlsx")

db_violin <- as.data.frame(db_violin)
db_violin$Domande <- as.factor(db_violin$Domande)

# Basic violin plot
basic_violin <- ggplot(db_violin, aes(x=Domande, y=Valori, fill=Domande)) + 
  geom_violin(trim = FALSE) +
  labs(title="Plot dei risultati del questionario psicometrico - Heatmap")

basic_violin + 
  # coord_flip() + 
  # per cambiare l'ordine dei violin plot nel grafico
  # scale_x_discrete(limits=c("Chiara", "Bella", "Utile",...))
  geom_violin(trim=FALSE) + 
  # violin plot with dot plot. Binwidth è aggiunto solo per evitare
  # il warning che appariva
  # geom_dotplot(binaxis='y', stackdir='center', dotsize=1, binwidth = 0.2) +
  scale_fill_manual(values=c("#999999", 
                             "#E69F00", 
                             "#56B4E9", 
                             "#5a8b59", 
                             "#8db4c0", 
                             "#509997")) + 
  geom_jitter(shape=16, position=position_jitter(0.05)) + 
  scale_y_continuous(breaks = seq(-3,10,by=1)) + theme_minimal()



###########################################################################
# RAINCLOUD PLOTS
# https://z3tt.github.io/Rainclouds/
# https://github.com/RainCloudPlots/RainCloudPlots/blob/master/README.md
# https://www.cedricscherer.com/2021/06/06/visualizing-distributions-with-raincloud-plots-with-ggplot2/
library(ggdist)
library(gghalves)


ggplot(db_violin, aes(x=Domande, y=Valori, fill=Domande)) + 
  ggdist::stat_halfeye(adjust = .9, width = .3, .width = 0, justification = -.3, point_colour = NA) + 
  geom_boxplot(width = .1, outlier.shape = NA) +
  ggdist::stat_dots(side = "left", dotsize = .5, justification = 1.1, binwidth = .1) +
  #gghalves::geom_half_point(side = "l", range_scale = .75, alpha = .5) +
  scale_y_continuous(breaks = seq(-3,10,by=1)) + 
  theme_classic()
  #gghalves::



###   ###
### VISUALIZZAZIONI QUESTIONARIO PSICOMETRICO  ###
###   ###

##########################################################################
# https://github.com/DBertazioli/ARmeetup/blob/master/Visualizations/survey/corr_questionario_1.R
# Correlogramma

# create corr -------------------------------------------------------------
# install.packages("vctrs", repos=c("http://rstudio.org/_packages",
#                                   "http://cran.rstudio.com",dependencies=TRUE))

# Il corrplot è stato creato utilizzando TUTTI i dati a disposizione.

rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/1_prima_viz")


library(psych)
library(Hmisc)
library(readxl)
library(corrplot)
library(RColorBrewer)




# db_heatmap <- read_excel("1_prima_viz.xlsx")
db_heatmap <- read_excel("viz_CORR.xlsx")


db_heatmap <- db_heatmap[,c(-1, -2, -3,-4)]
colnames(db_heatmap)[6] <- "Complessivo"

mcor <- cor(db_heatmap)

corrplot(mcor, 
         method = "ellipse",
         type = 'lower',
         diag = TRUE,
         # se vuoi ruotare gli attributi
         tl.srt = 0,
         tl.cex = 1.1,
         tl.col = "black",
         addCoef.col ='white',
         col = brewer.pal(n = 8, name = "RdBu"),
         number.cex = 1.05,
         cl.pos="r")

### SINGOLI CORRELOGRAMMI ### ### ### ### ### ### ### ### ### ### ### ### ###
### PRIMA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/1_prima_viz")


library(psych)
library(Hmisc)
library(readxl)
library(corrplot)
library(RColorBrewer)

# db_heatmap <- read_excel("1_prima_viz.xlsx")
db_heatmap <- read_excel("1_prima_viz.xlsx")


db_heatmap <- db_heatmap[,c(-1, -2, -3,-4)]
colnames(db_heatmap)[6] <- "Complessivo"

mcor <- cor(db_heatmap)
title <- "Correlogramma della prima visualizzazione"


corrplot(mcor, 
         method = "ellipse",
         type = 'lower',
         diag = TRUE,
         title=title,
         mar=c(0,0,1,0), # http://stackoverflow.com/a/14754408/54964
         # se vuoi ruotare gli attributi
         tl.srt = 0,
         tl.cex = 1.1,
         tl.col = "black",
         addCoef.col ='white',
         col = brewer.pal(n = 8, name = "RdBu"),
         number.cex = 1.05,
         cl.pos="r")

# Spiegazione di mar=c(0,0,1,0):
# "A numerical vector of the form c(bottom, left, top, right) which gives 
# the number of lines of margin to be specified on the four sides of the plot. 
# The default is c(5, 4, 4, 2) + 0.1." 
# Link: https://stat.ethz.ch/R-manual/R-devel/library/graphics/html/par.html

### SECONDA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/2_seconda_viz")


library(psych)
library(Hmisc)
library(readxl)
library(corrplot)
library(RColorBrewer)

# db_heatmap <- read_excel("1_prima_viz.xlsx")
db_heatmap <- read_excel("2_seconda_viz.xlsx")


db_heatmap <- db_heatmap[,c(-1, -2, -3,-4)]
colnames(db_heatmap)[6] <- "Complessivo"

mcor <- cor(db_heatmap)
title <- "Correlogramma della seconda visualizzazione"


corrplot(mcor, 
         method = "ellipse",
         type = 'lower',
         diag = TRUE,
         title=title,
         mar=c(0,0,1,0), # http://stackoverflow.com/a/14754408/54964
         # se vuoi ruotare gli attributi
         tl.srt = 0,
         tl.cex = 1.1,
         tl.col = "black",
         addCoef.col ='white',
         col = brewer.pal(n = 8, name = "RdBu"),
         number.cex = 1.05,
         cl.pos="r")


### TERZA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/3_terza_viz")


library(psych)
library(Hmisc)
library(readxl)
library(corrplot)
library(RColorBrewer)

# db_heatmap <- read_excel("1_prima_viz.xlsx")
db_heatmap <- read_excel("3_terza_viz.xlsx")


db_heatmap <- db_heatmap[,c(-1, -2, -3,-4)]
colnames(db_heatmap)[6] <- "Complessivo"

mcor <- cor(db_heatmap)
title <- "Correlogramma della terza visualizzazione"

corrplot(mcor, 
         method = "ellipse",
         type = 'lower',
         diag = TRUE,
         title=title,
         mar=c(0,0,1,0), # http://stackoverflow.com/a/14754408/54964
         # se vuoi ruotare gli attributi
         tl.srt = 0,
         tl.cex = 1.1,
         tl.col = "black",
         addCoef.col ='white',
         col = brewer.pal(n = 8, name = "RdBu"),
         number.cex = 1.05,
         cl.pos="r")

### QUARTA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/4_quarta_viz")


library(psych)
library(Hmisc)
library(readxl)
library(corrplot)
library(RColorBrewer)

# db_heatmap <- read_excel("1_prima_viz.xlsx")
db_heatmap <- read_excel("4_quarta_viz.xlsx")


db_heatmap <- db_heatmap[,c(-1, -2, -3,-4)]
colnames(db_heatmap)[6] <- "Complessivo"

mcor <- cor(db_heatmap)
title <- "Correlogramma della quarta visualizzazione"

corrplot(mcor, 
         method = "ellipse",
         type = 'lower',
         diag = TRUE,
         title=title,
         mar=c(0,0,1,0), # http://stackoverflow.com/a/14754408/54964
         # se vuoi ruotare gli attributi
         tl.srt = 0,
         tl.cex = 1.1,
         tl.col = "black",
         addCoef.col ='white',
         col = brewer.pal(n = 8, name = "RdBu"),
         number.cex = 1.05,
         cl.pos="r")


### QUINTA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/5_quinta_viz")


library(psych)
library(Hmisc)
library(readxl)
library(corrplot)
library(RColorBrewer)

# db_heatmap <- read_excel("1_prima_viz.xlsx")
db_heatmap <- read_excel("5_quinta_viz.xlsx")


db_heatmap <- db_heatmap[,c(-1, -2, -3,-4)]
colnames(db_heatmap)[6] <- "Complessivo"

mcor <- cor(db_heatmap)
title <- "Correlogramma della quinta visualizzazione"

corrplot(mcor, 
         method = "ellipse",
         type = 'lower',
         diag = TRUE,
         title=title,
         mar=c(0,0,1,0), # http://stackoverflow.com/a/14754408/54964
         # se vuoi ruotare gli attributi
         tl.srt = 0,
         tl.cex = 1.1,
         tl.col = "black",
         addCoef.col ='white',
         col = brewer.pal(n = 8, name = "RdBu"),
         number.cex = 1.05,
         cl.pos="r")










###########################################################################
###########################################################################
###########################################################################
### PRIMA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###

## Likert chart ###
# https://stackoverflow.com/questions/48340901/using-likert-package-in-r-for-analyzing-real-survey-data
# https://bookdown.org/Rmadillo/likert/always-visualize.html
# https://xang1234.github.io/likert/
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/1_prima_viz")

library(dplyr)
library(readxl)
library(likert)
library(graphics)
require(grid)
require(lattice)
require(latticeExtra)
require(HH)

likert_db <- read_excel("1.viz_likert.xlsx")

lik_chart <- likert(Misure ~ .,data=likert_db, ylab=NULL, ReferenceZero=2,
       as.percent=TRUE,
       main = list("Likert chart per la Heatmap", x=unit(.55, "npc")),
       sub= list("Categorie", x=unit(.51, "npc")),
       xlim=c(-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100),
       xlab = "Percentuale",
       strip=FALSE,
       par.strip.text=list(cex=.7))

lik_chart


### SECONDA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
# https://xang1234.github.io/likert/
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/2_seconda_viz")

library(dplyr)
library(readxl)
library(likert)
library(graphics)
require(grid)
require(lattice)
require(latticeExtra)
require(HH)

likert_db <- read_excel("2.viz_likert.xlsx")


lik_chart <- likert(Misure ~ .,data=likert_db, ylab=NULL, ReferenceZero=2,
                    as.percent=TRUE,
                    main = list("Likert chart per il Lollipop", x=unit(.55, "npc")),
                    sub= list("Categorie", x=unit(.51, "npc")),
                    xlim=c(-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100),
                    xlab = "Percentuale",
                    strip=FALSE,
                    par.strip.text=list(cex=.7))

lik_chart


### TERZA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/3_terza_viz")

library(dplyr)
library(readxl)
library(likert)
library(graphics)
require(grid)
require(lattice)
require(latticeExtra)
require(HH)

likert_db <- read_excel("3.viz_likert.xlsx")

lik_chart <- likert(Misure ~ .,data=likert_db, ylab=NULL, ReferenceZero=2,
                    as.percent=TRUE,
                    main = list("Likert chart per Alluvial diagram", x=unit(.55, "npc")),
                    sub= list("Categorie", x=unit(.51, "npc")),
                    xlim=c(-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100),
                    xlab = "Percentuale",
                    strip=FALSE,
                    par.strip.text=list(cex=.7))

lik_chart


### QUARTA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/4_quarta_viz")

library(dplyr)
library(readxl)
library(likert)
library(graphics)
require(grid)
require(lattice)
require(latticeExtra)
require(HH)

likert_db <- read_excel("4.viz_likert.xlsx")

lik_chart <- likert(Misure ~ .,data=likert_db, ylab=NULL, ReferenceZero=2,
                    as.percent=TRUE,
                    main = list("Likert chart per Scatterplot", x=unit(.55, "npc")),
                    sub= list("Categorie", x=unit(.51, "npc")),
                    xlim=c(-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100),
                    xlab = "Percentuale",
                    strip=FALSE,
                    par.strip.text=list(cex=.7))

lik_chart


### QUINTA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/5_quinta_viz")

library(dplyr)
library(readxl)
library(likert)
library(graphics)
require(grid)
require(lattice)
require(latticeExtra)
require(HH)

likert_db <- read_excel("5.viz_likert.xlsx")

lik_chart <- likert(Misure ~ .,data=likert_db, ylab=NULL, ReferenceZero=2,
                    as.percent=TRUE,
                    main = list("Likert chart per Boxplot/Barplot", x=unit(.55, "npc")),
                    sub= list("Categorie", x=unit(.51, "npc")),
                    xlim=c(-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100),
                    xlab = "Percentuale",
                    strip=FALSE,
                    par.strip.text=list(cex=.7))

lik_chart


###############################################################################
###############################################################################
###############################################################################
### USER TEST VIOLIN PLOT CON RISPOSTE CORRETTE E NON CORRETTE PIù BANDA DI
### NORMALITà (CON MEDIA E 1 DEVIAZIONE STANDARD DA INSERIRE COME LINEE)
# Palette: https://www.color-hex.com/color-palettes/
### PRIMA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/1_prima_viz")

library(readxl)
library(ggplot2)



db_violin_user_test <- read_excel("1.viz_User_test.xlsx")

db_violin_user_test <- as.data.frame(db_violin_user_test)

db_violin_user_test$Utente <- as.factor(db_violin_user_test$Utente)
db_violin_user_test$Task <- as.factor(db_violin_user_test$Task)
db_violin_user_test$Corretto <- as.factor(db_violin_user_test$Corretto)

# Basic violin plot
basic_violin <- ggplot(db_violin_user_test, aes(x=Task, y=Tempo)) + 
  geom_violin(trim = F, 
              fill = '#f4f3ed', 
              color = '#a3bdbd', 
              alpha = 0.8) +
  labs(title="Plot dei risultati dello User test - Heatmap") +
  geom_boxplot(notch = F, 
               width=0.25, 
               fill = '#e5e5e5',
               color='#14213d',
               outlier.shape = NA, 
               alpha = 0.2) +
  scale_color_manual(values = c('#142cd7','#d73a24'),
                     name = "Risposte", 
                     labels = c('Corrette', 'Non corrette')) +
  labs(x = 'Task 1 - Heatmap', y = 'Tempo (s)') + 
  geom_jitter(aes(color = Corretto), 
              shape=16,
              position=position_jitter(0)) + 
  scale_y_continuous(breaks = seq(0, 300, by=25)) + 
  # Dovrebbe servire ad aggiungere una linea orizzontale al plot
  geom_hline(yintercept=53.63, 
             linetype = "dashed") +
  # Annotate dovrebbe servire ad aggiungere la fascia di normalità grigia
  annotate("rect", xmin = 0, xmax = 2, ymin = 42.56, ymax = 64.70,
           alpha = .3) +
  theme_minimal() +
  theme(axis.text.x=element_blank())


# su powerpoint aggiungere i riferimenti a media, mu + sigma e mu - sigma
basic_violin 

  

### SECONDA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/2_seconda_viz")

library(readxl)
library(ggplot2)



db_violin_user_test <- read_excel("2.viz_User_test.xlsx")

db_violin_user_test <- as.data.frame(db_violin_user_test)

db_violin_user_test$Utente <- as.factor(db_violin_user_test$Utente)
db_violin_user_test$Task <- as.factor(db_violin_user_test$Task)
db_violin_user_test$Corretto <- as.factor(db_violin_user_test$Corretto)

# Basic violin plot
basic_violin <- ggplot(db_violin_user_test, aes(x=Task, y=Tempo)) + 
  geom_violin(trim = F, 
              fill = '#f4f3ed', 
              color = '#a3bdbd', 
              alpha = 0.8) +
  labs(title="Plot dei risultati dello User test - Lollipop chart") +
  geom_boxplot(notch = F, 
               width=0.25, 
               fill = '#e5e5e5',
               color='#14213d',
               outlier.shape = NA, 
               alpha = 0.2) +
  scale_color_manual(values = c('#142cd7','#d73a24'),
                     name = "Risposte", 
                     labels = c('Corrette', 'Non corrette')) +
  labs(x = 'Task 2 - Lollipop', y = 'Tempo (s)') + 
  geom_jitter(aes(color = Corretto), 
              shape=16,
              position=position_jitter(0)) + 
  scale_y_continuous(breaks = seq(0, 130, by=25)) + 
  # Dovrebbe servire ad aggiungere una linea orizzontale al plot
  geom_hline(yintercept=30.03,
             linetype = "dashed") +
  # Annotate dovrebbe servire ad aggiungere la fascia di normalità grigia
  annotate("rect", xmin = 0, xmax = 2, ymin = 24.67, ymax = 35.39,
           alpha = .3) +
  theme_minimal() +
  theme(axis.text.x=element_blank())


# su powerpoint aggiungere i riferimenti a media, mu + sigma e mu - sigma
basic_violin 



### TERZA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/3_terza_viz")

library(readxl)
library(ggplot2)



db_violin_user_test <- read_excel("3.viz_User_test.xlsx")

db_violin_user_test <- as.data.frame(db_violin_user_test)

db_violin_user_test$Utente <- as.factor(db_violin_user_test$Utente)
db_violin_user_test$Task <- as.factor(db_violin_user_test$Task)
db_violin_user_test$Corretto <- as.factor(db_violin_user_test$Corretto)

# Basic violin plot
basic_violin <- ggplot(db_violin_user_test, aes(x=Task, y=Tempo)) + 
  geom_violin(trim = T, 
              fill = '#f4f3ed', 
              color = '#a3bdbd', 
              alpha = 0.8) +
  labs(title="Plot dei risultati dello User test - Alluvial diagram") +
  geom_boxplot(notch = F, 
               width=0.25, 
               fill = '#e5e5e5',
               color='#14213d',
               outlier.shape = NA, 
               alpha = 0.2) +
  scale_color_manual(values = c('#142cd7','#d73a24'),
                     name = "Risposte", 
                     labels = c('Corrette', 'Non corrette')) +
  labs(x = 'Task 3 - Alluvial', y = 'Tempo (s)') + 
  geom_jitter(aes(color = Corretto), 
              shape=16,
              position=position_jitter(0)) + 
  scale_y_continuous(breaks = seq(0, 130, by=25)) + 
  # Dovrebbe servire ad aggiungere una linea orizzontale al plot
  geom_hline(yintercept=43.40,
             linetype = "dashed") +
  # Annotate dovrebbe servire ad aggiungere la fascia di normalità grigia
  annotate("rect", xmin = 0, xmax = 2, ymin = 40.56, ymax = 46.24,
           alpha = .3) +
  theme_minimal() +
  theme(axis.text.x=element_blank())


# su powerpoint aggiungere i riferimenti a media, mu + sigma e mu - sigma
basic_violin 


### QUARTA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/4_quarta_viz")

library(readxl)
library(ggplot2)



db_violin_user_test <- read_excel("4.viz_User_test.xlsx")

db_violin_user_test <- as.data.frame(db_violin_user_test)

db_violin_user_test$Utente <- as.factor(db_violin_user_test$Utente)
db_violin_user_test$Task <- as.factor(db_violin_user_test$Task)
db_violin_user_test$Corretto <- as.factor(db_violin_user_test$Corretto)

# Basic violin plot
basic_violin <- ggplot(db_violin_user_test, aes(x=Task, y=Tempo)) + 
  geom_violin(trim = F, 
              fill = '#f4f3ed', 
              color = '#a3bdbd', 
              alpha = 0.8) +
  labs(title="Plot dei risultati dello User test - Scatterplot") +
  geom_boxplot(notch = F, 
               width=0.25, 
               fill = '#e5e5e5',
               color='#14213d',
               outlier.shape = NA, 
               alpha = 0.2) +
  scale_color_manual(values = c('#142cd7','#d73a24'),
                     name = "Risposte", 
                     labels = c('Corrette', 'Non corrette')) +
  labs(x = 'Task 4 - Scatterplot', y = 'Tempo (s)') + 
  geom_jitter(aes(color = Corretto), 
              shape=16,
              position=position_jitter(0)) + 
  scale_y_continuous(breaks = seq(0, 230, by=25)) + 
  # Dovrebbe servire ad aggiungere una linea orizzontale al plot
  geom_hline(yintercept=32.66,
             linetype = "dashed") +
  # Annotate dovrebbe servire ad aggiungere la fascia di normalità grigia
  annotate("rect", xmin = 0, xmax = 2, ymin = 26.44, ymax = 38.89,
           alpha = .3) +
  theme_minimal() +
  theme(axis.text.x=element_blank())


# su powerpoint aggiungere i riferimenti a media, mu + sigma e mu - sigma
basic_violin 



### QUINTA VISUALIZZAZIONE ### ### ### ### ### ### ### ### ### ### ### ### ###
rm(list=ls())
setwd("C:/Users/-M-/Desktop/DM_DV_Maggio/finale/Valutazioni_DATAVIZ/5_quinta_viz")

library(readxl)
library(ggplot2)



db_violin_user_test <- read_excel("5.viz_User_test.xlsx")

db_violin_user_test <- as.data.frame(db_violin_user_test)

db_violin_user_test$Utente <- as.factor(db_violin_user_test$Utente)
db_violin_user_test$Task <- as.factor(db_violin_user_test$Task)
db_violin_user_test$Corretto <- as.factor(db_violin_user_test$Corretto)

# Basic violin plot
basic_violin <- ggplot(db_violin_user_test, aes(x=Task, y=Tempo)) + 
  geom_violin(trim = F, 
              fill = '#f4f3ed', 
              color = '#a3bdbd', 
              alpha = 0.8) +
  labs(title="Plot dei risultati dello User test - Boxplot/Barplot") +
  geom_boxplot(notch = F, 
               width=0.25, 
               fill = '#e5e5e5',
               color='#14213d',
               outlier.shape = NA, 
               alpha = 0.2) +
  scale_color_manual(values = c('#142cd7','#d73a24'),
                     name = "Risposte", 
                     labels = c('Corrette', 'Non corrette')) +
  labs(x = 'Task 5 - Boxplot/Barplot', y = 'Tempo (s)') + 
  geom_jitter(aes(color = Corretto), 
              shape=16,
              position=position_jitter(0)) + 
  #scale_y_continuous(breaks = seq(0, 450, by=50)) + 
  # Dovrebbe servire ad aggiungere una linea orizzontale al plot
  geom_hline(yintercept=76.26,
             linetype = "dashed") +
  # Annotate dovrebbe servire ad aggiungere la fascia di normalità grigia
  annotate("rect", xmin = 0, xmax = 2, ymin = 66.58, ymax = 85.93,
           alpha = .3) +
  theme_minimal() +
  theme(axis.text.x=element_blank())


# su powerpoint aggiungere i riferimenti a media, mu + sigma e mu - sigma
basic_violin 



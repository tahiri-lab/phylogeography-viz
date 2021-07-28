library(shiny)
library(tidyverse)
library(plotly)
library(DT)
library(readr)
library(shinythemes)

#####Import Data
# data source: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/SN5DAP

dat<-read.table("Meteorology.csv", header = TRUE, sep = "\t")
dat<- dat %>% select(c("id_country","country","ccode","date","cases","deaths","temperature",
                       "radiation","precipitation","humidity","wind"))
dat<-drop_na(dat)

#####Make my app

# Define the user interface

ui <- navbarPage("My Application",
                 theme = shinytheme("united"),
                 
                 tabPanel("Page 1",
                          fluidRow(
                            column(3,
                                   selectInput("select", label = h3("Select Region"), 
                                               choices = list("Australia" = 1, "	Austria" = 2, "Belgium" = 3, "Canada" = 5,
                                                              "Switzerland" = 6, "Chile" = 7, "Colombia" = 8,
                                                              "Czechia"=10, "Germany"=11,"	Denmark"=12)
                                   ),
                                   #dateRangeInput("daterange1", "Date range:",
                                    #              start  = "2020-05-01",
                                    #              end    = "2020-05-17",
                                    #              min    = "2020-01-01",
                                    #              max    = "2020-07-27",
                                    #              format = "mm/dd/yyyy",
                                     #             separator = " - ")
                                   ),
                            column(9, 
                                   DT::dataTableOutput("p1_table", height = 500))
                          )),
                 
                 tabPanel("Page 2",
                          
                          sidebarPanel(
                            checkboxGroupInput("checkRegion", 
                                               h3("Select Region"), 
                                               choices = list("Australia" = 1, "	Austria" = 2, "Belgium" = 3, "Canada" = 5,
                                                              "Switzerland" = 6, "Chile" = 7, "Colombia" = 8,
                                                              "Czechia"=10, "Germany"=11,"	Denmark"=12),
                                               selected = "Australia"
                            )
                          ),
                          
                          mainPanel(
                            tabsetPanel(
                              tabPanel("Temperature", plotOutput("p2_temp")),
                              tabPanel("Radiation", plotOutput("p2_rad")),
                              tabPanel("Precipitation", plotOutput("p2_precip")),
                              tabPanel("Humidity", plotOutput("p2_humid")),
                              tabPanel("Wind", plotOutput("p2_wind"))
                              
                            )
                          )
                 ),
                 
                 tabPanel("Page 3",
                          fluidRow(
                            column(1, 
                                   radioButtons("radio_region", "Select Region:",
                                                c("Australia" = 1, "	Austria" = 2, "Belgium" = 3, "Canada" = 5,
                                                  "Switzerland" = 6, "Chile" = 7, "Colombia" = 8,
                                                  "Czechia"=10, "Germany"=11,"	Denmark"=12),
                                                selected = "Australia")
                                   ),
                            column(11, 
                                   plotOutput("p3_final"))
                          ))
                 
)


# Define the server function

server<-function(input,output){
  
  # For page 1
  
  output$p1_table = DT::renderDataTable({
    #date.range <- seq.Date(input$daterange1[1], input$daterange1[2], by = "day")
    filter(dat, id_country %in% input$select)
  })
  
  # For page 2
  output$p2_temp <- renderPlot({
    dat_temp <- filter(dat, id_country %in% input$checkRegion)
    ggplot(dat_temp,aes(y=cases,x=temperature)) + geom_point() +
      geom_smooth(method=lm) + 
      labs(title = "Reationship between Cases and Temperature", y = "Number of Cases", x="Temperature")
  })
  
  output$p2_rad <- renderPlot({
    dat_rad <- filter(dat, id_country %in% input$checkRegion)
    ggplot(dat_rad,aes(y=cases,x=radiation)) + geom_point() +
      geom_smooth(method=lm) + 
      labs(title = "Reationship between Cases and Radiation", y = "Number of Cases", x="Radiation")
  })
 
  output$p2_precip <- renderPlot({
    dat_precip <- filter(dat, id_country %in% input$checkRegion)
    ggplot(dat_precip,aes(y=cases,x=precipitation)) + geom_point() +
      geom_smooth(method=lm) + 
      labs(title = "Reationship between Cases and Precipitation", y = "Number of Cases", x="Precipitation")
  })
  
  output$p2_humid <- renderPlot({
    dat_humid <- filter(dat, id_country %in% input$checkRegion)
    ggplot(dat_humid,aes(y=cases,x=humidity)) + geom_point() +
      geom_smooth(method=lm) + 
      labs(title = "Reationship between Cases and Humidity", y = "Number of Cases", x="Humidity")
  })
  
  output$p2_wind <- renderPlot({
    dat_wind <- filter(dat, id_country %in% input$checkRegion)
    ggplot(dat_wind,aes(y=cases,x=wind)) + geom_point() +
      geom_smooth(method=lm) + 
      labs(title = "Reationship between Cases and Wind", y = "Number of Cases", x="Wind")
  })
  
  # For page 3 
  output$p3_final <- renderPlot({
    dat_final <- filter(dat, id_country %in% input$radio_region)
    ggplot(dat_final,aes(x=date,y=deaths)) + 
      geom_point() +
      theme(axis.text.x = element_text(size = 6, face = "bold", angle = 90))
      
  })
  
} 

shinyApp(ui,server)
import streamlit as st
import Algos as ag
import keywordsum as kw
import visualize_entites as ve

st.markdown("""
<style>
.st-emotion-cache-1avcm0n 
{
    visibility : hidden;
    height : 0rem;
}
            
.st-emotion-cache-1y4p8pa
{
    padding: 0rem 0rem 2rem;
}

</style>
""",unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;padding: 0rem 0px 1rem;'>TEXT SUMMARIZER</h1>",unsafe_allow_html=True)

keyWords = ["Algorithms","KeyWord","Entities"]
selectedType = st.selectbox("Type", keyWords, index=0)

def Algorithm():
  selectedAlog = st.selectbox("Algorithm", ag.algoArray, index=0)
  inputText =  st.text_area("Text to Summerize", height=180)
  
  if inputText == "" or inputText == None:
    ag.summary = ""
  
  if 'changed' not in st.session_state:
     st.session_state.changed = False
  
  def OnChanged():
      st.session_state.changed = True
  
  summerize_clicked = st.button("Summarize",use_container_width=True)
  
  container = st.container(border=True,height=180)
  col1,col2,col3 = container.columns([2,2,1])
  
  selectedLang = col3.selectbox("Languages", ag.langs, index=0,label_visibility="collapsed",on_change=OnChanged)

  if summerize_clicked and inputText and selectedAlog:
    ag.Summerize(inputText, selectedAlog)
    output = ag.summary
  
    if selectedLang != "en" and selectedLang != None:
      st.session_state.changed = False  
      output = ag.TranslateText(output, selectedLang)
  
    container.markdown(f'''{output}''',unsafe_allow_html=True)
  else :
    container.markdown("")

  if st.session_state.changed and ag.summary and selectedLang:  
    translated_summary = ag.TranslateText(ag.summary, selectedLang)
    container.markdown(f'''{translated_summary}''',unsafe_allow_html=True)
  else :
    container.markdown("")

def KeyWords():
  container = st.container(border=False,height=68)
  col1,col2,col3 = container.columns([2,2,2])
  # keywordText =  col1.text_area("Keyword", height=1,placeholder="Enter single KeyWord Here (EX : SUMMARIZER)")
  keywordText =  col1.text_input("Keyword", value="Single Word KeyWord",max_chars=30)
  inputText =  st.text_area("Text to Summerize", height=180)

  if inputText == "" or inputText == None:
    kw.summary = ""
    
  summerize_clicked = st.button("Summarize",use_container_width=True)

  print(f"summerize clicked = {summerize_clicked}\n")

  if summerize_clicked and inputText and keywordText:
    print(f"summerize clicked = {summerize_clicked},inputText : {inputText}, keywordText : {keywordText}\n")
    kw.summarize_text(inputText,keywordText,50)

  container = st.container(border=True,height=180)

  if  kw.summary == "400":  
    container.markdown("Coudn't Generate Summary Please make sure you are giving a single keyword and keyword has to be in the summary")
  elif kw.summary:
    container.markdown(f'''{kw.summary}''',unsafe_allow_html=True)
  else:
    container.markdown("")

def Entity():
  inputText =  st.text_area("Text to Summerize", height=180)
  entity_clicked = st.button("Generate",use_container_width=True)

  if entity_clicked:
    ve.visualize_entities(inputText)



print(f"Selected Type = {selectedType}\n")

if(selectedType == keyWords[0]):
  Algorithm()
elif (selectedType == keyWords[1]):
  KeyWords()
elif selectedType == keyWords[2]:
  Entity()

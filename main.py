import streamlit as st
from openai import OpenAI

api_key = st.secrets['OPENAI_API']
client = OpenAI(api_key=api_key)


def generate_story(prompt):
  story = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {
              "role":
              "system",
              "content":
              """You are bestseller sotry writer. You will
    take user's prompt and generate a short story for people of age early 20s"""
          },
          {
              "role": "user",
              "content": prompt
          }  #User Input
      ],
      max_tokens=400,
      temperature=0.5)

  return story.choices[0].message.content


def generate_image_comment(story):
  design = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {
              "role":
              "system",
              "content":
              """Base on the sotry given, you will design a 
     detailed image for the cover of this sotry. The image prompt should
    include the theme of the storyu with relevant color, suitable for adults.
    Theouoput should be between 100 characters."""
          },
          {
              "role": "user",
              "content": story
          }  #User Input
      ],
      max_tokens=400,
      temperature=0.5)

  return design.choices[0].message.content


def generate_image(image_description):
  cover_response = client.images.generate(model='dall-e-2',
                                          prompt=image_description,
                                          size="256x256",
                                          quality='standard',
                                          n=1)

  image_url = cover_response.data[0].url
  return image_url

st.title("AI Story Generator with Cover")

with st.form('lol'):
  st.write("This is for user to key in information")
  msg = st.text_input(label='Some keywords to generate a story')
  submitted = st.form_submit_button('Submit')

  if submitted:
    story = generate_story(msg)
    refined_prompt = generate_image_comment(story)
    image_url = generate_image(refined_prompt)
    st.image(image_url)
    st.write(story)

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from sklearn.metrics import precision_score, recall_score 

def main():
    st.title('Binary Classification Web App')
    st.sidebar.title('Binary Classification Web App')
    st.markdown('Are your Mushrooms Edible? 🍄')
    st.sidebar.markdown('Are your Mushrooms Edible? 🍄')

    @st.cache(persist=True)
    def load_data():
        data = pd.read_csv("C:/Users/DELL/Desktop/Mushrooms project/mushrooms.csv")
        label = LabelEncoder()
        for col in data.columns:
            data[col] = label.fit_transform(data[col])
        return data

    @st.cache(persist=True)
    def split(df):
        y = df.type
        x = df.drop(columns=['type'])
        x_train,x_test,y_train,y_test = train_test_split(x, y, test_size = 0.3, random_state=0)
        return x_train,x_test,y_train,y_test


    def plot_metrics(metrics_list):
        if 'Confusion Matrix' in metrics_list:
            st.subheader('Confusion Matrix')
            plot_confusion_matrix(model,x_test,y_test,display_labels=class_names)
            st.pyplot()

        if 'ROC Curve' in metrics_list:
            st.subheader('ROC Curve')
            plot_roc_curve(model,x_test,y_test)
            st.pyplot()

        if 'Precision-Recall Curve' in metrics_list:
            st.subheader('Precision-Recall Curve')
            plot_precision_recall_curve(model,x_test,y_test)
            st.pyplot()


        
    df = load_data()
    x_train,x_test,y_train,y_test = split(df)
    class_names=['edible','poisonous']
    st.sidebar.subheader('Choose Classifier')
    classifier = st.sidebar.selectbox('Classifier',('Support Vector Classifier (SVM)','Logistic Regression','Random Forest'))

    if  classifier == 'Support Vector Classifier (SVM)':
        st.sidebar.subheader('Model Hyperparameter')
        C = st.sidebar.number_input('C(Regularisation Parameter)',0.01,10.0,step=0.01,key = 'C')
        kernel = st.sidebar.radio('Kernel',("rbf","linear"),key='kernel')
        gamma = st.sidebar.radio('Gamma(Kernel Coefficient)',('scale','auto'),key='gamma')

        metrics = st.sidebar.multiselect("What matrics to plot?",('Confusion Matrix', 'ROC Curve','Precision-Recall Curve'))

        if st.sidebar.button("Classify",key='classify'):
            st.subheader('Support Vector Classifier (SVM) Results')
            model = SVC(C=C, kernel=kernel, gamma=gamma)
            model.fit(x_train,y_train)
            accuracy= model.score(x_test,y_test)
            y_pred=model.predict(x_test)
            st.write("Accuracy: ",accuracy.round(2))
            st.write("Precision: ",precision_score(y_test,y_pred,labels=class_names).round(2))
            st.write("Recall: ",recall_score(y_test,y_pred,labels=class_names).round(2))
            plot_metrics(metrics)


    if  classifier == 'Logistic Regression':
        st.sidebar.subheader('Model Hyperparameter')
        C = st.sidebar.number_input('C(Regularisation Parameter)',0.01,10.0,step=0.01,key = 'C_LR')
        max_iter = st.sidebar.slider("Maximum number of Iterations",100,500,key='max_iter')

        metrics = st.sidebar.multiselect("What matrics to plot?",('Confusion Matrix', 'ROC Curve','Precision-Recall Curve'))

        if st.sidebar.button("Classify",key='classify'):
            st.subheader('Logistic Regression Results')
            model = LogisticRegression(C=C,max_iter=max_iter)
            model.fit(x_train,y_train)
            accuracy= model.score(x_test,y_test)
            y_pred=model.predict(x_test)
            st.write("Accuracy: ",accuracy.round(2))
            st.write("Precision: ",precision_score(y_test,y_pred,labels=class_names).round(2))
            st.write("Recall: ",recall_score(y_test,y_pred,labels=class_names).round(2))
            plot_metrics(metrics)

    if  classifier == 'Random Forest':
        st.sidebar.subheader('Model Hyperparameter')
        n_estimators = st.sidebar.number_input('The Number Of Trees in the Forest',100,5000,step=10,key='n_estimators')
        max_dept = st.sidebar.number_input("The Maximum dept of the Tree",1,20,step=1,key='max_dept')
        bootstrap = st.sidebar.radio('Bootstrap Samples when building trees',('True','False'),key='bootstrap')
        metrics = st.sidebar.multiselect("What matrics to plot?",('Confusion Matrix', 'ROC Curve','Precision-Recall Curve'))

        if st.sidebar.button("Classify",key='classify'):
            st.subheader('Random Forest Results')
            model = RandomForestClassifier(n_estimators=n_estimators,max_depth=max_dept,bootstrap=bootstrap,n_jobs=-1)
            model.fit(x_train,y_train)
            accuracy= model.score(x_test,y_test)
            y_pred=model.predict(x_test)
            st.write("Accuracy: ",accuracy.round(2))
            st.write("Precision: ",precision_score(y_test,y_pred,labels=class_names).round(2))
            st.write("Recall: ",recall_score(y_test,y_pred,labels=class_names).round(2))
            plot_metrics(metrics)

















    if st.sidebar.checkbox('Show raw data', False):
        st.subheader('Mushroom Dataset (Classification)')
        st.write(df)
        






if __name__ == '__main__':
    main()



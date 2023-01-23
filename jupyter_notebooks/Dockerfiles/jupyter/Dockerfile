#FROM continuumio/anaconda3
FROM condaforge/mambaforge
COPY . .
#RUN conda env create -n myenv -f "./optimal_limits/environment.yml"
# RUN conda install -c conda-forge -y mamba
RUN mamba install -y jupyter  jupyterlab
RUN mamba install -c conda-forge -y cudatoolkit==11.2
RUN mamba install -c conda-forge -y yfinance voila
EXPOSE 8888
COPY jupyter_lab_config.py /root/.jupyter/jupyter_lab_config.py
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
#ENTRYPOINT [ "mecury", "watch", "./optimal_limits/optimal_limits.ipynb"]
#/opt/conda/bin/mercury
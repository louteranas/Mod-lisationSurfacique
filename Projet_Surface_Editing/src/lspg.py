# Module lspg
"""
Contient des utilisatires de gestion des évènements pour pygame
Version 0.1
"""
import pygame
_version=0.1

def lspgloop(verbose=False) :
   """
   Entre adna sla boucle des évènement et attend que
   l'utilisateur referme la fenêtre. La paramètre optionnel verbose, s'il
   est égal à True, affiche le contenu des évènements traités dans al boucle.
   """
   done=False
   while not done:
        for event in pygame.event.get():
           if verbose : print("lspg : ",event)
           if event.type == pygame.QUIT: done=True 
            

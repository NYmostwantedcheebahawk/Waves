import Waves.filter_editor.utilities.transform as transform

DEFAULT_HPTFX = "default.hptfx"


class Data:

    def __init__(self, filter_editor, transform_func_file=None):
        """
        Initialise la classe de Data
        :param filter_editor: fichier des données temporelles
        :param transform_func_file: -> fichier de type .xml > contient des fonctions de transformation sauvegardees
        """
        if transform_func_file is None:
            """
            import_func_type: -> string > le type de fonction dans la pipeline par exemple: csv
            transformations: -> transformation[] > ceci est la pipeline browser contenant toute les objets data et leur type de transformation subie.
            """
            self.transformations = [filter_editor]
        else:
            """
            si transform_func_file contient deja des data
            """
            self.transformations = []
            self.read_hptfx(transform_func_file, filter_editor)
            self.current_index = 0


    def insert_transformation(self, cls, index=-1, *args, **kwargs):
        """
        Insert une transformation dans la liste des transformations
        :param cls: une classe de type Tranformation (mais pas ImportFile)
        :param index: indice où insérer la nouvelle transformation dans la liste
        :param args: arguments pour l'initialisation de la classe cls
        :param kwargs: arguments pour l'initialisation de la classe cls
        :return:
        """
        func = cls(*args, **kwargs)
        if index == -1:
            self.transformations.append(func(self.transformations[index]))
        else:
            self.transformations.insert(index, func(self.transformations[index]))
            self.recalculate_data_through_pipeline(index)

    def recalculate_data_through_pipeline(self, idx=0):
        """
        Recalculer les données dans la liste de transformations
        chaque fois qu une transformation est ajoutee ou retiree
        :param idx: Endroit à partir du quel on recalcule
        """
        for i in range(idx, len(self.transformations)):
            self.transformations[i] = self.transformations[i](self.transformations[i - 1])
